"""
Z80/Z80N instruction implementation for vForth emulator
Instruction reference: Z80 User Manual, Z80N extensions

IMPORTANT - canonical Z80 semantics:
  CALL/RET operate on the Z80 hardware stack (SP). In vForth, SP doubles as the
  Forth calculation-stack pointer, but that is irrelevant to these opcodes: they
  behave exactly like real hardware. The Forth EXIT word is a SEPARATE CODE word
  (made of ex de,hl / ld c,(hl) / ... / jp (ix)), NOT opcode 0xC9.
  EXECUTE is literally a single `ret` (0xC9): it pops the xt from SP into PC.

Flag register F (bit layout):
  7=S  6=Z  5=F5  4=H  3=F3  2=P/V  1=N  0=C
"""

# Flag bit masks
FLAG_S = 0x80   # sign     (bit 7 of result)
FLAG_Z = 0x40   # zero     (result == 0)
FLAG_5 = 0x20   # undocumented copy of result bit 5
FLAG_H = 0x10   # half carry
FLAG_3 = 0x08   # undocumented copy of result bit 3
FLAG_PV = 0x04  # parity / overflow
FLAG_N = 0x02   # add(0)/subtract(1)
FLAG_C = 0x01   # carry


def _parity_even(v):
    """Return True if v (8-bit) has an even number of set bits (P/V parity)."""
    v &= 0xFF
    p = 1
    while v:
        p ^= 1
        v &= v - 1
    return p == 1


# --- 8-bit ALU flag helpers (return the 8-bit result, set cpu.F canonically) ---

def _add8(cpu, a, b, carry=0):
    res = a + b + carry
    r = res & 0xFF
    f = 0
    if r & 0x80:
        f |= FLAG_S
    if r == 0:
        f |= FLAG_Z
    f |= r & (FLAG_5 | FLAG_3)
    if ((a & 0x0F) + (b & 0x0F) + carry) & 0x10:
        f |= FLAG_H
    if (~(a ^ b) & (a ^ r)) & 0x80:
        f |= FLAG_PV
    if res & 0x100:
        f |= FLAG_C
    cpu.F = f  # N = 0
    return r


def _sub8(cpu, a, b, carry=0):
    res = a - b - carry
    r = res & 0xFF
    f = FLAG_N
    if r & 0x80:
        f |= FLAG_S
    if r == 0:
        f |= FLAG_Z
    f |= r & (FLAG_5 | FLAG_3)
    if ((a & 0x0F) - (b & 0x0F) - carry) & 0x10:
        f |= FLAG_H
    if ((a ^ b) & (a ^ r)) & 0x80:
        f |= FLAG_PV
    if res & 0x100:
        f |= FLAG_C  # borrow
    cpu.F = f
    return r


def _cp8(cpu, a, b):
    """CP: flags as for (A - b) but result is discarded. F3/F5 come from b."""
    res = a - b
    r = res & 0xFF
    f = FLAG_N
    if r & 0x80:
        f |= FLAG_S
    if r == 0:
        f |= FLAG_Z
    f |= b & (FLAG_5 | FLAG_3)
    if ((a & 0x0F) - (b & 0x0F)) & 0x10:
        f |= FLAG_H
    if ((a ^ b) & (a ^ r)) & 0x80:
        f |= FLAG_PV
    if res & 0x100:
        f |= FLAG_C
    cpu.F = f


def _logic8(cpu, result, hflag):
    """Flags for AND (hflag=True) / OR / XOR (hflag=False). C=0, N=0, P/V=parity."""
    r = result & 0xFF
    f = 0
    if r & 0x80:
        f |= FLAG_S
    if r == 0:
        f |= FLAG_Z
    f |= r & (FLAG_5 | FLAG_3)
    if hflag:
        f |= FLAG_H
    if _parity_even(r):
        f |= FLAG_PV
    cpu.F = f
    return r


def _inc8(cpu, v):
    r = (v + 1) & 0xFF
    f = cpu.F & FLAG_C  # carry preserved
    if r & 0x80:
        f |= FLAG_S
    if r == 0:
        f |= FLAG_Z
    f |= r & (FLAG_5 | FLAG_3)
    if (v & 0x0F) == 0x0F:
        f |= FLAG_H
    if v == 0x7F:
        f |= FLAG_PV
    cpu.F = f  # N = 0
    return r


def _dec8(cpu, v):
    r = (v - 1) & 0xFF
    f = (cpu.F & FLAG_C) | FLAG_N  # carry preserved, N = 1
    if r & 0x80:
        f |= FLAG_S
    if r == 0:
        f |= FLAG_Z
    f |= r & (FLAG_5 | FLAG_3)
    if (v & 0x0F) == 0x00:
        f |= FLAG_H
    if v == 0x80:
        f |= FLAG_PV
    cpu.F = f
    return r


# --- 16-bit ALU flag helpers ---

def _add16(cpu, a, b):
    """ADD HL,rr: affects H,N,C and F3/F5; S,Z,P/V preserved."""
    res = a + b
    r = res & 0xFFFF
    f = cpu.F & (FLAG_S | FLAG_Z | FLAG_PV)
    f |= (r >> 8) & (FLAG_5 | FLAG_3)
    if ((a & 0x0FFF) + (b & 0x0FFF)) & 0x1000:
        f |= FLAG_H
    if res & 0x10000:
        f |= FLAG_C
    cpu.F = f  # N = 0
    return r


def _adc16(cpu, a, b):
    carry = 1 if (cpu.F & FLAG_C) else 0
    res = a + b + carry
    r = res & 0xFFFF
    f = 0
    if r & 0x8000:
        f |= FLAG_S
    if r == 0:
        f |= FLAG_Z
    f |= (r >> 8) & (FLAG_5 | FLAG_3)
    if ((a & 0x0FFF) + (b & 0x0FFF) + carry) & 0x1000:
        f |= FLAG_H
    if (~(a ^ b) & (a ^ r)) & 0x8000:
        f |= FLAG_PV
    if res & 0x10000:
        f |= FLAG_C
    cpu.F = f  # N = 0
    return r


def _sbc16(cpu, a, b):
    carry = 1 if (cpu.F & FLAG_C) else 0
    res = a - b - carry
    r = res & 0xFFFF
    f = FLAG_N
    if r & 0x8000:
        f |= FLAG_S
    if r == 0:
        f |= FLAG_Z
    f |= (r >> 8) & (FLAG_5 | FLAG_3)
    if ((a & 0x0FFF) - (b & 0x0FFF) - carry) & 0x1000:
        f |= FLAG_H
    if ((a ^ b) & (a ^ r)) & 0x8000:
        f |= FLAG_PV
    if res & 0x10000:
        f |= FLAG_C
    cpu.F = f
    return r


def inst_nop(cpu):
    """0x00: NOP - no operation"""
    pass


def inst_ld_bc_nn(cpu):
    """0x01 nn: LD BC,nn - load immediate 16-bit"""
    lo = cpu.fetch_byte()
    hi = cpu.fetch_byte()
    cpu.BC = lo | (hi << 8)


def inst_ld_de_nn(cpu):
    """0x11 nn: LD DE,nn - load immediate 16-bit"""
    lo = cpu.fetch_byte()
    hi = cpu.fetch_byte()
    cpu.DE = lo | (hi << 8)


def inst_ld_hl_nn(cpu):
    """0x21 nn: LD HL,nn - load immediate 16-bit"""
    lo = cpu.fetch_byte()
    hi = cpu.fetch_byte()
    cpu.HL = lo | (hi << 8)


def inst_ld_sp_nn(cpu):
    """0x31 nn: LD SP,nn - load stack pointer"""
    lo = cpu.fetch_byte()
    hi = cpu.fetch_byte()
    cpu.SP = lo | (hi << 8)


def inst_ld_a_bcm(cpu):
    """0x0A: LD A,(BC) - load A from memory at BC"""
    cpu.A = cpu.mem[cpu.BC]


def inst_ld_a_dem(cpu):
    """0x1A: LD A,(DE) - load A from memory at DE"""
    cpu.A = cpu.mem[cpu.DE]


def inst_ld_a_hlm(cpu):
    """0x7E: LD A,(HL) - load A from memory at HL"""
    cpu.A = cpu.mem[cpu.HL]


def inst_ld_l_hlm(cpu):
    """0x6E: LD L,(HL) - load L from memory at HL"""
    cpu.L = cpu.mem[cpu.HL]


def inst_ld_a_d(cpu):
    """0x7A: LD A,D - copy D to A"""
    cpu.A = cpu.D


def inst_ld_l_a(cpu):
    """0x6F: LD L,A - copy A to L"""
    cpu.L = cpu.A


def inst_ld_h_a(cpu):
    """0x67: LD H,A - copy A to H"""
    cpu.H = cpu.A


def inst_ld_c_a(cpu):
    """0x4F: LD C,A - copy A to C"""
    cpu.C = cpu.A


def inst_ld_a_c(cpu):
    """0x79: LD A,C - copy C to A"""
    cpu.A = cpu.C


def inst_ld_a_b(cpu):
    """0x78: LD A,B - copy B to A"""
    cpu.A = cpu.B


def inst_ld_b_a(cpu):
    """0x47: LD B,A - copy B to A"""
    cpu.B = cpu.A


def inst_push_bc(cpu):
    """0xC5: PUSH BC - push BC onto stack"""
    cpu.push(cpu.BC)


def inst_push_de(cpu):
    """0xD5: PUSH DE - push DE onto stack"""
    cpu.push(cpu.DE)


def inst_push_hl(cpu):
    """0xE5: PUSH HL - push HL onto stack"""
    cpu.push(cpu.HL)


def inst_push_af(cpu):
    """0xF5: PUSH AF - push AF onto stack"""
    cpu.push((cpu.A << 8) | cpu.F)


def inst_pop_bc(cpu):
    """0xC1: POP BC - pop BC from stack"""
    cpu.BC = cpu.pop()


def inst_pop_de(cpu):
    """0xD1: POP DE - pop DE from stack"""
    cpu.DE = cpu.pop()


def inst_pop_hl(cpu):
    """0xE1: POP HL - pop HL from stack"""
    cpu.HL = cpu.pop()


def inst_pop_af(cpu):
    """0xF1: POP AF - pop AF from stack"""
    val = cpu.pop()
    cpu.A = (val >> 8) & 0xFF
    cpu.F = val & 0xFF


def inst_inc_bc(cpu):
    """0x03: INC BC - increment BC"""
    cpu.BC = (cpu.BC + 1) & 0xFFFF


def inst_inc_de(cpu):
    """0x13: INC DE - increment DE"""
    cpu.DE = (cpu.DE + 1) & 0xFFFF


def inst_inc_hl(cpu):
    """0x23: INC HL - increment HL"""
    cpu.HL = (cpu.HL + 1) & 0xFFFF


def inst_inc_sp(cpu):
    """0x33: INC SP - increment SP"""
    cpu.SP = (cpu.SP + 1) & 0xFFFF


def inst_inc_a(cpu):
    """0x3C: INC A - increment A"""
    cpu.A = _inc8(cpu, cpu.A)


def inst_dec_a(cpu):
    """0x3D: DEC A - decrement A"""
    cpu.A = _dec8(cpu, cpu.A)


def inst_ld_hlm_a(cpu):
    """0x77: LD (HL),A - store A into memory at HL"""
    cpu.mem[cpu.HL] = cpu.A & 0xFF


def inst_jp_nn(cpu):
    """0xC3 nn: JP nn - jump to address"""
    lo = cpu.fetch_byte()
    hi = cpu.fetch_byte()
    cpu.PC = lo | (hi << 8)


def inst_jp_hl(cpu):
    """0xE9: JP (HL) - jump to address in HL"""
    cpu.PC = cpu.HL


def inst_exx(cpu):
    """0xD9: EXX - exchange main and alternate registers"""
    cpu.BC, cpu.BC_alt = cpu.BC_alt, cpu.BC
    cpu.DE, cpu.DE_alt = cpu.DE_alt, cpu.DE
    cpu.HL, cpu.HL_alt = cpu.HL_alt, cpu.HL


def inst_halt(cpu):
    """0x76: HALT - wait for the next interrupt, then continue.

    On the ZX Spectrum, `ei halt` (e.g. the 1FRAME word) waits for the 50Hz
    frame interrupt and then resumes at the following instruction. We do not
    model the hardware interrupt, so the interrupt is treated as firing
    immediately: HALT simply proceeds. (Frame-sync delays collapse to zero,
    which is fine for headless functional emulation.)
    """
    cpu.frame_count = getattr(cpu, 'frame_count', 0) + 1


def inst_or_a(cpu):
    """0xB7: OR A - OR A with itself (test A; clears C, sets Z if A==0)"""
    cpu.A = _logic8(cpu, cpu.A | cpu.A, False)


def inst_cp_a(cpu):
    """0xBF: CP A - compare A with itself (always equal: Z=1, C=0, N=1)"""
    _cp8(cpu, cpu.A, cpu.A)


def inst_xor_a(cpu):
    """0xAF: XOR A - XOR A with itself (clear A; Z=1, C=0)"""
    cpu.A = _logic8(cpu, 0, False)


def inst_and_a(cpu):
    """0xA7: AND A - AND A with itself (test A; clears C, sets Z if A==0, H=1)"""
    cpu.A = _logic8(cpu, cpu.A & cpu.A, True)


def inst_ld_a_nn(cpu):
    """0x3A nn: LD A,(nn) - load A from memory at nn"""
    lo = cpu.fetch_byte()
    hi = cpu.fetch_byte()
    addr = lo | (hi << 8)
    cpu.A = cpu.mem[addr]


def inst_ld_nn_a(cpu):
    """0x32 nn: LD (nn),A - store A into memory at nn"""
    lo = cpu.fetch_byte()
    hi = cpu.fetch_byte()
    addr = lo | (hi << 8)
    cpu.mem[addr] = cpu.A & 0xFF


def inst_inc_b(cpu):
    """0x04: INC B - increment B"""
    cpu.B = _inc8(cpu, cpu.B)


def inst_inc_c(cpu):
    """0x0C: INC C - increment C"""
    cpu.C = _inc8(cpu, cpu.C)


def inst_inc_d(cpu):
    """0x14: INC D - increment D"""
    cpu.D = _inc8(cpu, cpu.D)


def inst_inc_e(cpu):
    """0x1C: INC E - increment E"""
    cpu.E = _inc8(cpu, cpu.E)


def inst_inc_h(cpu):
    """0x24: INC H - increment H"""
    cpu.H = _inc8(cpu, cpu.H)


def inst_inc_l(cpu):
    """0x2C: INC L - increment L"""
    cpu.L = _inc8(cpu, cpu.L)


def inst_inc_hlm(cpu):
    """0x34: INC (HL) - increment memory at HL"""
    cpu.mem[cpu.HL] = _inc8(cpu, cpu.mem[cpu.HL])


def inst_dec_b(cpu):
    """0x05: DEC B - decrement B"""
    cpu.B = _dec8(cpu, cpu.B)


def inst_dec_c(cpu):
    """0x0D: DEC C - decrement C"""
    cpu.C = _dec8(cpu, cpu.C)


def inst_dec_d(cpu):
    """0x15: DEC D - decrement D"""
    cpu.D = _dec8(cpu, cpu.D)


def inst_dec_e(cpu):
    """0x1D: DEC E - decrement E"""
    cpu.E = _dec8(cpu, cpu.E)


def inst_dec_h(cpu):
    """0x25: DEC H - decrement H"""
    cpu.H = _dec8(cpu, cpu.H)


def inst_dec_l(cpu):
    """0x2D: DEC L - decrement L"""
    cpu.L = _dec8(cpu, cpu.L)


def inst_dec_hlm(cpu):
    """0x35: DEC (HL) - decrement memory at HL"""
    cpu.mem[cpu.HL] = _dec8(cpu, cpu.mem[cpu.HL])


def inst_ld_b_nn(cpu):
    """0x06 n: LD B,n - load immediate 8-bit"""
    cpu.B = cpu.fetch_byte()


def inst_ld_c_nn(cpu):
    """0x0E n: LD C,n - load immediate 8-bit"""
    cpu.C = cpu.fetch_byte()


def inst_ld_d_nn(cpu):
    """0x16 n: LD D,n - load immediate 8-bit"""
    cpu.D = cpu.fetch_byte()


def inst_ld_e_nn(cpu):
    """0x1E n: LD E,n - load immediate 8-bit"""
    cpu.E = cpu.fetch_byte()


def inst_ld_h_nn(cpu):
    """0x26 n: LD H,n - load immediate 8-bit"""
    cpu.H = cpu.fetch_byte()


def inst_ld_l_nn(cpu):
    """0x2E n: LD L,n - load immediate 8-bit"""
    cpu.L = cpu.fetch_byte()


def inst_ld_hlm_nn(cpu):
    """0x36 n: LD (HL),n - store immediate 8-bit into memory at HL"""
    val = cpu.fetch_byte()
    cpu.mem[cpu.HL] = val


def inst_call_nn(cpu):
    """0xCD nn: CALL nn - canonical Z80 call: push return address on SP, jump.

    This is plain hardware behaviour. The vForth `call Enter_Ptr` mechanism
    relies on it: Enter_Ptr does `pop bc` to retrieve the PFA pushed here.
    """
    lo = cpu.fetch_byte()
    hi = cpu.fetch_byte()
    addr = lo | (hi << 8)
    cpu.push(cpu.PC)
    cpu.PC = addr


def inst_ret(cpu):
    """0xC9: RET - canonical Z80 return: PC = pop(SP).

    NOT the Forth EXIT (which is a separate CODE word operating on DE).
    EXECUTE is a single RET: it pops the xt from SP into PC.
    upper^ ends with RET as a normal subroutine return.
    """
    cpu.PC = cpu.pop()


def inst_ret_nz(cpu):
    """0xC0: RET NZ"""
    if not (cpu.F & FLAG_Z):
        cpu.PC = cpu.pop()


def inst_ret_z(cpu):
    """0xC8: RET Z"""
    if cpu.F & FLAG_Z:
        cpu.PC = cpu.pop()


def inst_ret_nc(cpu):
    """0xD0: RET NC - used by upper^ (case-folding routine)"""
    if not (cpu.F & FLAG_C):
        cpu.PC = cpu.pop()


def inst_ret_c(cpu):
    """0xD8: RET C - used by upper^ (case-folding routine)"""
    if cpu.F & FLAG_C:
        cpu.PC = cpu.pop()


def inst_call_nz_nn(cpu):
    """0xC4 nn: CALL NZ,nn"""
    lo = cpu.fetch_byte()
    hi = cpu.fetch_byte()
    addr = lo | (hi << 8)
    if not (cpu.F & FLAG_Z):
        cpu.push(cpu.PC)
        cpu.PC = addr


def inst_call_z_nn(cpu):
    """0xCC nn: CALL Z,nn"""
    lo = cpu.fetch_byte()
    hi = cpu.fetch_byte()
    addr = lo | (hi << 8)
    if cpu.F & FLAG_Z:
        cpu.push(cpu.PC)
        cpu.PC = addr


def inst_call_nc_nn(cpu):
    """0xD4 nn: CALL NC,nn"""
    lo = cpu.fetch_byte()
    hi = cpu.fetch_byte()
    addr = lo | (hi << 8)
    if not (cpu.F & FLAG_C):
        cpu.push(cpu.PC)
        cpu.PC = addr


def inst_call_c_nn(cpu):
    """0xDC nn: CALL C,nn"""
    lo = cpu.fetch_byte()
    hi = cpu.fetch_byte()
    addr = lo | (hi << 8)
    if cpu.F & FLAG_C:
        cpu.push(cpu.PC)
        cpu.PC = addr


def inst_jp_nz_nn(cpu):
    """0xC2 nn: JP NZ,nn - jump if not zero"""
    lo = cpu.fetch_byte()
    hi = cpu.fetch_byte()
    addr = lo | (hi << 8)
    if not (cpu.F & 0x40):  # Z flag not set
        cpu.PC = addr


def inst_jp_z_nn(cpu):
    """0xCA nn: JP Z,nn - jump if zero"""
    lo = cpu.fetch_byte()
    hi = cpu.fetch_byte()
    addr = lo | (hi << 8)
    if cpu.F & 0x40:  # Z flag set
        cpu.PC = addr


def inst_jp_nc_nn(cpu):
    """0xD2 nn: JP NC,nn - jump if no carry"""
    lo = cpu.fetch_byte()
    hi = cpu.fetch_byte()
    addr = lo | (hi << 8)
    if not (cpu.F & 0x01):  # C flag not set
        cpu.PC = addr


def inst_jp_c_nn(cpu):
    """0xDA nn: JP C,nn - jump if carry"""
    lo = cpu.fetch_byte()
    hi = cpu.fetch_byte()
    addr = lo | (hi << 8)
    if cpu.F & 0x01:  # C flag set
        cpu.PC = addr


def inst_ld_b_c(cpu):
    """0x41: LD B,C - copy C to B"""
    cpu.B = cpu.C


def inst_ld_c_b(cpu):
    """0x48: LD C,B - copy B to C"""
    cpu.C = cpu.B


def inst_ld_b_d(cpu):
    """0x42: LD B,D - copy D to B"""
    cpu.B = cpu.D


def inst_ld_d_b(cpu):
    """0x50: LD D,B - copy B to D"""
    cpu.D = cpu.B


def inst_ld_b_e(cpu):
    """0x43: LD B,E - copy E to B"""
    cpu.B = cpu.E


def inst_ld_e_b(cpu):
    """0x58: LD E,B - copy B to E"""
    cpu.E = cpu.B


def inst_add_a_b(cpu):
    """0x80: ADD A,B - add B to A"""
    cpu.A = _add8(cpu, cpu.A, cpu.B)


def inst_add_a_c(cpu):
    """0x81: ADD A,C - add C to A"""
    cpu.A = _add8(cpu, cpu.A, cpu.C)


def inst_add_a_d(cpu):
    """0x82: ADD A,D - add D to A"""
    cpu.A = _add8(cpu, cpu.A, cpu.D)


def inst_add_a_e(cpu):
    """0x83: ADD A,E - add E to A"""
    cpu.A = _add8(cpu, cpu.A, cpu.E)


def inst_sub_a_b(cpu):
    """0x90: SUB A,B - subtract B from A"""
    cpu.A = _sub8(cpu, cpu.A, cpu.B)


def inst_sub_a_c(cpu):
    """0x91: SUB A,C - subtract C from A"""
    cpu.A = _sub8(cpu, cpu.A, cpu.C)


def inst_ld_bc_a(cpu):
    """0x02: LD (BC),A - store A into memory at BC"""
    cpu.mem[cpu.BC] = cpu.A & 0xFF


def inst_ld_de_a(cpu):
    """0x12: LD (DE),A - store A into memory at DE"""
    cpu.mem[cpu.DE] = cpu.A & 0xFF


def inst_dec_bc(cpu):
    """0x0B: DEC BC - decrement BC"""
    cpu.BC = (cpu.BC - 1) & 0xFFFF


def inst_dec_de(cpu):
    """0x1B: DEC DE - decrement DE"""
    cpu.DE = (cpu.DE - 1) & 0xFFFF


def inst_dec_hl(cpu):
    """0x2B: DEC HL - decrement HL"""
    cpu.HL = (cpu.HL - 1) & 0xFFFF


def inst_dec_sp(cpu):
    """0x3B: DEC SP - decrement SP"""
    cpu.SP = (cpu.SP - 1) & 0xFFFF


def inst_ld_hl_b(cpu):
    """0x70: LD (HL),B - store B into memory at HL"""
    cpu.mem[cpu.HL] = cpu.B & 0xFF


def inst_ld_hl_c(cpu):
    """0x71: LD (HL),C - store C into memory at HL"""
    cpu.mem[cpu.HL] = cpu.C & 0xFF


def inst_ld_hl_d(cpu):
    """0x72: LD (HL),D - store D into memory at HL"""
    cpu.mem[cpu.HL] = cpu.D & 0xFF


def inst_ld_hl_e(cpu):
    """0x73: LD (HL),E - store E into memory at HL"""
    cpu.mem[cpu.HL] = cpu.E & 0xFF


def inst_ld_hl_h(cpu):
    """0x74: LD (HL),H - store H into memory at HL"""
    cpu.mem[cpu.HL] = cpu.H & 0xFF


def inst_ld_hl_l(cpu):
    """0x75: LD (HL),L - store L into memory at HL"""
    cpu.mem[cpu.HL] = cpu.L & 0xFF


def inst_ld_b_hlm(cpu):
    """0x46: LD B,(HL) - load B from memory at HL"""
    cpu.B = cpu.mem[cpu.HL]


def inst_ld_c_hlm(cpu):
    """0x4E: LD C,(HL) - load C from memory at HL"""
    cpu.C = cpu.mem[cpu.HL]


def inst_ld_d_hlm(cpu):
    """0x56: LD D,(HL) - load D from memory at HL"""
    cpu.D = cpu.mem[cpu.HL]


def inst_ld_e_hlm(cpu):
    """0x5E: LD E,(HL) - load E from memory at HL"""
    cpu.E = cpu.mem[cpu.HL]


def inst_ld_h_hlm(cpu):
    """0x66: LD H,(HL) - load H from memory at HL"""
    cpu.H = cpu.mem[cpu.HL]


def inst_ex_de_hl(cpu):
    """0xEB: EX DE,HL - exchange DE and HL"""
    cpu.DE, cpu.HL = cpu.HL, cpu.DE


def inst_jr_c_n(cpu):
    """0x38 n: JR C,n - jump relative if carry"""
    disp = cpu.fetch_byte()
    if disp & 0x80:
        disp -= 0x100
    if cpu.F & 0x01:  # C flag set
        cpu.PC = (cpu.PC + disp) & 0xFFFF


def inst_jr_nc_n(cpu):
    """0x30 n: JR NC,n - jump relative if no carry"""
    disp = cpu.fetch_byte()
    if disp & 0x80:
        disp -= 0x100
    if not (cpu.F & 0x01):  # C flag not set
        cpu.PC = (cpu.PC + disp) & 0xFFFF


def inst_jr_z_n(cpu):
    """0x28 n: JR Z,n - jump relative if zero"""
    disp = cpu.fetch_byte()
    if disp & 0x80:
        disp -= 0x100
    if cpu.F & 0x40:  # Z flag set
        cpu.PC = (cpu.PC + disp) & 0xFFFF


def inst_jr_nz_n(cpu):
    """0x20 n: JR NZ,n - jump relative if not zero"""
    disp = cpu.fetch_byte()
    if disp & 0x80:
        disp -= 0x100
    if not (cpu.F & 0x40):  # Z flag not set
        cpu.PC = (cpu.PC + disp) & 0xFFFF


def inst_jr_n(cpu):
    """0x18 n: JR n - jump relative"""
    disp = cpu.fetch_byte()
    if disp & 0x80:
        disp -= 0x100
    cpu.PC = (cpu.PC + disp) & 0xFFFF


def inst_djnz(cpu):
    """0x10 d: DJNZ d - decrement B; jump relative if B != 0. Flags unaffected.

    Used by inc/ms.f (the millisecond delay loop: `10 C, FD C,` = DJNZ -3).
    The displacement is measured from the byte after the operand, exactly as
    JR -- so it is added to PC once the operand has been fetched.
    """
    disp = cpu.fetch_byte()
    if disp & 0x80:
        disp -= 0x100
    cpu.B = (cpu.B - 1) & 0xFF
    if cpu.B != 0:
        cpu.PC = (cpu.PC + disp) & 0xFFFF


def inst_ld_hl_nnm(cpu):
    """0x2A nn: LD HL,(nn) - load HL from memory at nn"""
    lo = cpu.fetch_byte()
    hi = cpu.fetch_byte()
    addr = lo | (hi << 8)
    cpu.HL = cpu.mem16_le(addr)


def inst_ld_bc_nnm(cpu):
    """0xED 0x4B nn: LD BC,(nn) - load BC from memory at nn.
    (Duplicate of _ld_bc_nn_mem, which is the one registered at ED 4B.)"""
    lo = cpu.fetch_byte()
    hi = cpu.fetch_byte()
    addr = lo | (hi << 8)
    cpu.BC = cpu.mem16_le(addr)


def inst_ld_nnm_hl(cpu):
    """0x22 nn: LD (nn),HL - store HL into memory at nn"""
    lo = cpu.fetch_byte()
    hi = cpu.fetch_byte()
    addr = lo | (hi << 8)
    cpu.mem16_le_set(addr, cpu.HL)


def inst_ld_nnm_bc(cpu):
    """0xED 0x43 nn: LD (nn),BC - store BC into memory at nn.
    (Duplicate of _ld_nn_bc, which is the one registered at ED 43.)"""
    lo = cpu.fetch_byte()
    hi = cpu.fetch_byte()
    addr = lo | (hi << 8)
    cpu.mem16_le_set(addr, cpu.BC)


def inst_sub_a_h(cpu):
    """0x94: SUB A,H - subtract H from A"""
    cpu.A = _sub8(cpu, cpu.A, cpu.H)


def inst_sub_a_l(cpu):
    """0x95: SUB A,L - subtract L from A"""
    cpu.A = _sub8(cpu, cpu.A, cpu.L)


def inst_sub_a_hlm(cpu):
    """0x96: SUB A,(HL) - subtract memory at HL from A"""
    cpu.A = _sub8(cpu, cpu.A, cpu.mem[cpu.HL])


def inst_sub_a_nn(cpu):
    """0xD6 n: SUB A,n - subtract immediate from A"""
    val = cpu.fetch_byte()
    cpu.A = _sub8(cpu, cpu.A, val)


def inst_add_a_h(cpu):
    """0x84: ADD A,H - add H to A"""
    cpu.A = _add8(cpu, cpu.A, cpu.H)


def inst_add_a_l(cpu):
    """0x85: ADD A,L - add L to A"""
    cpu.A = _add8(cpu, cpu.A, cpu.L)


def inst_add_a_hlm(cpu):
    """0x86: ADD A,(HL) - add memory at HL to A"""
    cpu.A = _add8(cpu, cpu.A, cpu.mem[cpu.HL])


def inst_add_a_nn(cpu):
    """0xC6 n: ADD A,n - add immediate to A"""
    val = cpu.fetch_byte()
    cpu.A = _add8(cpu, cpu.A, val)


def inst_cp_nn(cpu):
    """0xFE n: CP n - compare A with immediate (sets flags, A unchanged)"""
    val = cpu.fetch_byte()
    _cp8(cpu, cpu.A, val)


def inst_cp_hlm(cpu):
    """0xBE: CP (HL) - compare A with memory at HL (sets flags, A unchanged)"""
    _cp8(cpu, cpu.A, cpu.mem[cpu.HL])


def inst_and_nn(cpu):
    """0xE6 n: AND A,n - AND A with immediate"""
    val = cpu.fetch_byte()
    cpu.A = _logic8(cpu, cpu.A & val, True)


def inst_or_nn(cpu):
    """0xF6 n: OR A,n - OR A with immediate"""
    val = cpu.fetch_byte()
    cpu.A = _logic8(cpu, cpu.A | val, False)


def inst_xor_nn(cpu):
    """0xEE n: XOR A,n - XOR A with immediate"""
    val = cpu.fetch_byte()
    cpu.A = _logic8(cpu, cpu.A ^ val, False)


def inst_add_hl_a(cpu):
    """0xED 0x31: ADD HL,A (Z80N) - HL = HL + A (A unsigned). Flags unaffected."""
    cpu.HL = (cpu.HL + cpu.A) & 0xFFFF


def inst_add_de_a_z80n(cpu):
    """0xED 0x32: ADD DE,A (Z80N) - DE = DE + A (A unsigned). Flags unaffected."""
    cpu.DE = (cpu.DE + cpu.A) & 0xFFFF


def inst_add_bc_a(cpu):
    """0xED 0x33: ADD BC,A (Z80N) - BC = BC + A (A unsigned). Flags unaffected."""
    cpu.BC = (cpu.BC + cpu.A) & 0xFFFF


def inst_add_hl_nn_z80n(cpu):
    """0xED 0x34 nn nn: ADD HL,nn (Z80N) - 16-bit immediate, little-endian. Flags unaffected."""
    lo = cpu.fetch_byte(); hi = cpu.fetch_byte()
    cpu.HL = (cpu.HL + (lo | (hi << 8))) & 0xFFFF


def inst_add_de_nn(cpu):
    """0xED 0x35 nn nn: ADD DE,nn (Z80N) - 16-bit immediate, little-endian. Flags unaffected."""
    lo = cpu.fetch_byte(); hi = cpu.fetch_byte()
    cpu.DE = (cpu.DE + (lo | (hi << 8))) & 0xFFFF


def inst_add_bc_nn(cpu):
    """0xED 0x36 nn nn: ADD BC,nn (Z80N) - 16-bit immediate, little-endian. Flags unaffected."""
    lo = cpu.fetch_byte(); hi = cpu.fetch_byte()
    cpu.BC = (cpu.BC + (lo | (hi << 8))) & 0xFFFF


def inst_bsla_de_b(cpu):
    """0xED 0x28: BSLA DE,B (Z80N) - barrel shift left DE by (B & 0x1F)."""
    n = cpu.B & 0x1F
    cpu.DE = (cpu.DE << n) & 0xFFFF


def inst_bsrl_de_b(cpu):
    """0xED 0x2A: BSRL DE,B (Z80N) - barrel shift right logical DE by (B & 0x1F)."""
    n = cpu.B & 0x1F
    cpu.DE = (cpu.DE >> n) & 0xFFFF


def inst_ld_a_e(cpu):
    """0x7B: LD A,E - copy E to A"""
    cpu.A = cpu.E


def inst_ld_a_h(cpu):
    """0x7C: LD A,H - copy H to A"""
    cpu.A = cpu.H


def inst_ld_a_l(cpu):
    """0x7D: LD A,L - copy L to A"""
    cpu.A = cpu.L


def inst_ld_d_a(cpu):
    """0x57: LD D,A - copy A to D"""
    cpu.D = cpu.A


def inst_ld_e_a(cpu):
    """0x5F: LD E,A - copy A to E"""
    cpu.E = cpu.A


def inst_ld_l_b(cpu):
    """0x68: LD L,B - copy B to L"""
    cpu.L = cpu.B


def inst_ld_l_c(cpu):
    """0x69: LD L,C - copy C to L"""
    cpu.L = cpu.C


def inst_ld_l_d(cpu):
    """0x6A: LD L,D - copy D to L"""
    cpu.L = cpu.D


def inst_ld_l_e(cpu):
    """0x6B: LD L,E - copy E to L"""
    cpu.L = cpu.E


def inst_ld_h_b(cpu):
    """0x60: LD H,B - copy B to H"""
    cpu.H = cpu.B


def inst_ld_h_c(cpu):
    """0x61: LD H,C - copy C to H"""
    cpu.H = cpu.C


def inst_ld_h_d(cpu):
    """0x62: LD H,D - copy D to H"""
    cpu.H = cpu.D


def inst_ld_h_e(cpu):
    """0x63: LD H,E - copy E to H"""
    cpu.H = cpu.E


def inst_add_hl_bc(cpu):
    """0x09: ADD HL,BC - add BC to HL"""
    cpu.HL = _add16(cpu, cpu.HL, cpu.BC)


def inst_add_hl_de(cpu):
    """0x19: ADD HL,DE - add DE to HL"""
    cpu.HL = _add16(cpu, cpu.HL, cpu.DE)


def inst_add_hl_hl(cpu):
    """0x29: ADD HL,HL - add HL to HL (shift left)"""
    cpu.HL = _add16(cpu, cpu.HL, cpu.HL)


def inst_add_hl_sp(cpu):
    """0x39: ADD HL,SP - add SP to HL"""
    cpu.HL = _add16(cpu, cpu.HL, cpu.SP)


def inst_or_a_b(cpu):
    """0xB0: OR A,B - OR A with B"""
    cpu.A = _logic8(cpu, cpu.A | cpu.B, False)


def inst_or_a_c(cpu):
    """0xB1: OR A,C - OR A with C"""
    cpu.A = _logic8(cpu, cpu.A | cpu.C, False)


def inst_or_a_d(cpu):
    """0xB2: OR A,D - OR A with D"""
    cpu.A = _logic8(cpu, cpu.A | cpu.D, False)


def inst_or_a_e(cpu):
    """0xB3: OR A,E - OR A with E"""
    cpu.A = _logic8(cpu, cpu.A | cpu.E, False)


def inst_or_a_h(cpu):
    """0xB4: OR A,H - OR A with H"""
    cpu.A = _logic8(cpu, cpu.A | cpu.H, False)


def inst_or_a_l(cpu):
    """0xB5: OR A,L - OR A with L"""
    cpu.A = _logic8(cpu, cpu.A | cpu.L, False)


def inst_or_a_hlm(cpu):
    """0xB6: OR A,(HL) - OR A with memory at HL"""
    cpu.A = _logic8(cpu, cpu.A | cpu.mem[cpu.HL], False)


def inst_and_a_b(cpu):
    """0xA0: AND A,B - AND A with B"""
    cpu.A = _logic8(cpu, cpu.A & cpu.B, True)


def inst_and_a_c(cpu):
    """0xA1: AND A,C - AND A with C"""
    cpu.A = _logic8(cpu, cpu.A & cpu.C, True)


def inst_and_a_d(cpu):
    """0xA2: AND A,D - AND A with D"""
    cpu.A = _logic8(cpu, cpu.A & cpu.D, True)


def inst_and_a_e(cpu):
    """0xA3: AND A,E - AND A with E"""
    cpu.A = _logic8(cpu, cpu.A & cpu.E, True)


def inst_and_a_h(cpu):
    """0xA4: AND A,H - AND A with H"""
    cpu.A = _logic8(cpu, cpu.A & cpu.H, True)


def inst_and_a_l(cpu):
    """0xA5: AND A,L - AND A with L"""
    cpu.A = _logic8(cpu, cpu.A & cpu.L, True)


def inst_and_a_hlm(cpu):
    """0xA6: AND A,(HL) - AND A with memory at HL"""
    cpu.A = _logic8(cpu, cpu.A & cpu.mem[cpu.HL], True)


def inst_xor_a_b(cpu):
    """0xA8: XOR A,B - XOR A with B"""
    cpu.A = _logic8(cpu, cpu.A ^ cpu.B, False)


def inst_xor_a_c(cpu):
    """0xA9: XOR A,C - XOR A with C"""
    cpu.A = _logic8(cpu, cpu.A ^ cpu.C, False)


def inst_xor_a_d(cpu):
    """0xAA: XOR A,D - XOR A with D"""
    cpu.A = _logic8(cpu, cpu.A ^ cpu.D, False)


def inst_xor_a_e(cpu):
    """0xAB: XOR A,E - XOR A with E"""
    cpu.A = _logic8(cpu, cpu.A ^ cpu.E, False)


def inst_xor_a_h(cpu):
    """0xAC: XOR A,H - XOR A with H"""
    cpu.A = _logic8(cpu, cpu.A ^ cpu.H, False)


def inst_xor_a_l(cpu):
    """0xAD: XOR A,L - XOR A with L"""
    cpu.A = _logic8(cpu, cpu.A ^ cpu.L, False)


def inst_xor_a_hlm(cpu):
    """0xAE: XOR A,(HL) - XOR A with memory at HL"""
    cpu.A = _logic8(cpu, cpu.A ^ cpu.mem[cpu.HL], False)


def inst_cp_a_b(cpu):
    """0xB8: CP A,B - compare A with B"""
    _cp8(cpu, cpu.A, cpu.B)


def inst_cp_a_c(cpu):
    """0xB9: CP A,C - compare A with C"""
    _cp8(cpu, cpu.A, cpu.C)


def inst_cp_a_d(cpu):
    """0xBA: CP A,D - compare A with D"""
    _cp8(cpu, cpu.A, cpu.D)


def inst_cp_a_e(cpu):
    """0xBB: CP A,E - compare A with E"""
    _cp8(cpu, cpu.A, cpu.E)


def inst_cp_a_h(cpu):
    """0xBC: CP A,H - compare A with H"""
    _cp8(cpu, cpu.A, cpu.H)


def inst_cp_a_l(cpu):
    """0xBD: CP A,L - compare A with L"""
    _cp8(cpu, cpu.A, cpu.L)


# Extended instructions (prefix 0xED)


def inst_nextreg_a(cpu):
    """0xED 0x92 n: NEXTREG n,A - write A to Next register n.

    Register 87 (MMU slot 7) is fully modelled: assigning cpu.mmu7_page
    swaps the $E000-$FFFF window content (see Z80CPU.mmu7_page)."""
    reg = cpu.fetch_byte()
    if reg == 87:  # MMU register for slot 7
        cpu.mmu7_page = cpu.A & 0xFF


def inst_nextreg_nn(cpu):
    """0xED 0x91 n m: NEXTREG n,m - write immediate m to Next register n"""
    reg = cpu.fetch_byte()
    val = cpu.fetch_byte()
    if reg == 87:
        cpu.mmu7_page = val & 0xFF


def inst_push_nn(cpu):
    """0xED 0x8A nn nn: PUSH nn (Z80N) - push 16-bit immediate.

    Note: the Z80N PUSH nn immediate is stored BIG-ENDIAN (high byte first).
    """
    hi = cpu.fetch_byte()
    lo = cpu.fetch_byte()
    cpu.push((hi << 8) | lo)


def inst_mul_de(cpu):
    """0xED 0x30: MUL D,E - multiply D*E -> DE (unsigned). Z80N: flags unaffected."""
    result = (cpu.D * cpu.E) & 0xFFFF
    cpu.DE = result


def inst_sbc_hl_bc(cpu):
    """0xED 0x42: SBC HL,BC"""
    cpu.HL = _sbc16(cpu, cpu.HL, cpu.BC)


def inst_sbc_hl_de(cpu):
    """0xED 0x52: SBC HL,DE"""
    cpu.HL = _sbc16(cpu, cpu.HL, cpu.DE)


def inst_sbc_hl_hl(cpu):
    """0xED 0x62: SBC HL,HL"""
    cpu.HL = _sbc16(cpu, cpu.HL, cpu.HL)


def inst_sbc_hl_sp(cpu):
    """0xED 0x72: SBC HL,SP"""
    cpu.HL = _sbc16(cpu, cpu.HL, cpu.SP)


def inst_adc_hl_bc(cpu):
    """0xED 0x4A: ADC HL,BC"""
    cpu.HL = _adc16(cpu, cpu.HL, cpu.BC)


def inst_adc_hl_de(cpu):
    """0xED 0x5A: ADC HL,DE"""
    cpu.HL = _adc16(cpu, cpu.HL, cpu.DE)


def inst_adc_hl_hl(cpu):
    """0xED 0x6A: ADC HL,HL"""
    cpu.HL = _adc16(cpu, cpu.HL, cpu.HL)


def inst_adc_hl_sp(cpu):
    """0xED 0x7A: ADC HL,SP"""
    cpu.HL = _adc16(cpu, cpu.HL, cpu.SP)


def inst_ld_de_nnm(cpu):
    """0xED 0x5B nn: LD DE,(nn) - load DE from memory at nn"""
    lo = cpu.fetch_byte()
    hi = cpu.fetch_byte()
    addr = lo | (hi << 8)
    cpu.DE = cpu.mem16_le(addr)


def inst_ld_nnm_sp(cpu):
    """0xED 0x73 nn: LD (nn),SP - store SP into memory at nn"""
    lo = cpu.fetch_byte()
    hi = cpu.fetch_byte()
    addr = lo | (hi << 8)
    cpu.mem16_le_set(addr, cpu.SP)


def inst_ld_sp_nnm(cpu):
    """0xED 0x7B nn: LD SP,(nn) - load SP from memory at nn"""
    lo = cpu.fetch_byte()
    hi = cpu.fetch_byte()
    addr = lo | (hi << 8)
    cpu.SP = cpu.mem16_le(addr)


# IX instructions (prefix 0xDD)
def inst_ld_ix_nn(cpu):
    """0xDD 0x21 nn: LD IX,nn - load immediate 16-bit"""
    lo = cpu.fetch_byte()
    hi = cpu.fetch_byte()
    cpu.IX = lo | (hi << 8)


def inst_ld_l_ixm_disp(cpu):
    """0xDD 0x6E d: LD L,(IX+d) - load L from memory at IX+displacement"""
    disp = cpu.fetch_byte()
    if disp & 0x80:
        disp -= 0x100
    addr = (cpu.IX + disp) & 0xFFFF
    cpu.L = cpu.mem[addr]


def inst_ld_h_ixm_disp(cpu):
    """0xDD 0x66 d: LD H,(IX+d) - load H from memory at IX+displacement"""
    disp = cpu.fetch_byte()
    if disp & 0x80:
        disp -= 0x100
    addr = (cpu.IX + disp) & 0xFFFF
    cpu.H = cpu.mem[addr]


def inst_jp_ix(cpu):
    """0xDD 0xE9: JP (IX) - jump to address in IX"""
    cpu.PC = cpu.IX


# Main dispatch table
INSTRUCTION_MAP = {
    0x00: inst_nop,
    0x01: inst_ld_bc_nn,
    0x02: inst_ld_bc_a,
    0x03: inst_inc_bc,
    0x04: inst_inc_b,
    0x05: inst_dec_b,
    0x06: inst_ld_b_nn,
    0x09: inst_add_hl_bc,
    0x0A: inst_ld_a_bcm,
    0x0B: inst_dec_bc,
    0x0C: inst_inc_c,
    0x0D: inst_dec_c,
    0x0E: inst_ld_c_nn,
    0x11: inst_ld_de_nn,
    0x12: inst_ld_de_a,
    0x13: inst_inc_de,
    0x14: inst_inc_d,
    0x15: inst_dec_d,
    0x16: inst_ld_d_nn,
    0x18: inst_jr_n,
    0x19: inst_add_hl_de,
    0x1A: inst_ld_a_dem,
    0x1B: inst_dec_de,
    0x1C: inst_inc_e,
    0x1D: inst_dec_e,
    0x1E: inst_ld_e_nn,
    0x20: inst_jr_nz_n,
    0x21: inst_ld_hl_nn,
    0x22: inst_ld_nnm_hl,
    0x23: inst_inc_hl,
    0x24: inst_inc_h,
    0x25: inst_dec_h,
    0x26: inst_ld_h_nn,
    0x28: inst_jr_z_n,
    0x29: inst_add_hl_hl,
    0x2A: inst_ld_hl_nnm,
    0x2B: inst_dec_hl,
    0x2C: inst_inc_l,
    0x2D: inst_dec_l,
    0x2E: inst_ld_l_nn,
    0x30: inst_jr_nc_n,
    0x31: inst_ld_sp_nn,
    0x32: inst_ld_nn_a,
    0x33: inst_inc_sp,
    0x34: inst_inc_hlm,
    0x35: inst_dec_hlm,
    0x36: inst_ld_hlm_nn,
    0x38: inst_jr_c_n,
    0x39: inst_add_hl_sp,
    0x3A: inst_ld_a_nn,
    0x3B: inst_dec_sp,
    0x3C: inst_inc_a,
    0x3D: inst_dec_a,
    0x41: inst_ld_b_c,
    0x42: inst_ld_b_d,
    0x43: inst_ld_b_e,
    0x46: inst_ld_b_hlm,
    0x47: inst_ld_b_a,
    0x48: inst_ld_c_b,
    0x4E: inst_ld_c_hlm,
    0x4F: inst_ld_c_a,
    0x50: inst_ld_d_b,
    0x56: inst_ld_d_hlm,
    0x57: inst_ld_d_a,
    0x58: inst_ld_e_b,
    0x5E: inst_ld_e_hlm,
    0x5F: inst_ld_e_a,
    0x60: inst_ld_h_b,
    0x61: inst_ld_h_c,
    0x62: inst_ld_h_d,
    0x63: inst_ld_h_e,
    0x66: inst_ld_h_hlm,
    0x67: inst_ld_h_a,
    0x68: inst_ld_l_b,
    0x69: inst_ld_l_c,
    0x6A: inst_ld_l_d,
    0x6B: inst_ld_l_e,
    0x6E: inst_ld_l_hlm,
    0x6F: inst_ld_l_a,
    0x70: inst_ld_hl_b,
    0x71: inst_ld_hl_c,
    0x72: inst_ld_hl_d,
    0x73: inst_ld_hl_e,
    0x74: inst_ld_hl_h,
    0x75: inst_ld_hl_l,
    0x77: inst_ld_hlm_a,
    0x78: inst_ld_a_b,
    0x79: inst_ld_a_c,
    0x7A: inst_ld_a_d,
    0x7B: inst_ld_a_e,
    0x7C: inst_ld_a_h,
    0x7D: inst_ld_a_l,
    0x7E: inst_ld_a_hlm,
    0x80: inst_add_a_b,
    0x81: inst_add_a_c,
    0x82: inst_add_a_d,
    0x83: inst_add_a_e,
    0x84: inst_add_a_h,
    0x85: inst_add_a_l,
    0x86: inst_add_a_hlm,
    0x90: inst_sub_a_b,
    0x91: inst_sub_a_c,
    0x94: inst_sub_a_h,
    0x95: inst_sub_a_l,
    0x96: inst_sub_a_hlm,
    0xA0: inst_and_a_b,
    0xA1: inst_and_a_c,
    0xA2: inst_and_a_d,
    0xA3: inst_and_a_e,
    0xA4: inst_and_a_h,
    0xA5: inst_and_a_l,
    0xA6: inst_and_a_hlm,
    0xA7: inst_and_a,
    0xA8: inst_xor_a_b,
    0xA9: inst_xor_a_c,
    0xAA: inst_xor_a_d,
    0xAB: inst_xor_a_e,
    0xAC: inst_xor_a_h,
    0xAD: inst_xor_a_l,
    0xAE: inst_xor_a_hlm,
    0xAF: inst_xor_a,
    0xB0: inst_or_a_b,
    0xB1: inst_or_a_c,
    0xB2: inst_or_a_d,
    0xB3: inst_or_a_e,
    0xB4: inst_or_a_h,
    0xB5: inst_or_a_l,
    0xB6: inst_or_a_hlm,
    0xB7: inst_or_a,
    0xB8: inst_cp_a_b,
    0xB9: inst_cp_a_c,
    0xBA: inst_cp_a_d,
    0xBB: inst_cp_a_e,
    0xBC: inst_cp_a_h,
    0xBD: inst_cp_a_l,
    0xBE: inst_cp_hlm,
    0xBF: inst_cp_a,
    0xC0: inst_ret_nz,
    0xC1: inst_pop_bc,
    0xC2: inst_jp_nz_nn,
    0xC3: inst_jp_nn,
    0xC4: inst_call_nz_nn,
    0xC5: inst_push_bc,
    0xC6: inst_add_a_nn,
    0xC8: inst_ret_z,
    0xC9: inst_ret,
    0xCA: inst_jp_z_nn,
    0xCC: inst_call_z_nn,
    0xCD: inst_call_nn,
    0xD0: inst_ret_nc,
    0xD1: inst_pop_de,
    0xD2: inst_jp_nc_nn,
    0xD4: inst_call_nc_nn,
    0xD5: inst_push_de,
    0xD6: inst_sub_a_nn,
    0xD8: inst_ret_c,
    0xD9: inst_exx,
    0xDA: inst_jp_c_nn,
    0xDC: inst_call_c_nn,
    0xEB: inst_ex_de_hl,
    0xE1: inst_pop_hl,
    0xE5: inst_push_hl,
    0xE6: inst_and_nn,
    0xE9: inst_jp_hl,
    0xEE: inst_xor_nn,
    0xF1: inst_pop_af,
    0xF5: inst_push_af,
    0xF6: inst_or_nn,
    0xFE: inst_cp_nn,
    0x76: inst_halt,
}

EXTENDED_MAP = {  # 0xED prefix
    # Z80N register arithmetic
    0x28: inst_bsla_de_b,    # BSLA DE,B
    0x2A: inst_bsrl_de_b,    # BSRL DE,B
    0x30: inst_mul_de,       # MUL D,E
    0x31: inst_add_hl_a,     # ADD HL,A
    0x32: inst_add_de_a_z80n,  # ADD DE,A
    0x33: inst_add_bc_a,     # ADD BC,A
    0x34: inst_add_hl_nn_z80n,  # ADD HL,nn
    0x35: inst_add_de_nn,    # ADD DE,nn
    0x36: inst_add_bc_nn,    # ADD BC,nn
    0x8A: inst_push_nn,      # PUSH nn (big-endian immediate)
    # Standard Z80 16-bit load / arithmetic
    0x42: inst_sbc_hl_bc,
    0x4A: inst_adc_hl_bc,
    0x52: inst_sbc_hl_de,
    0x5A: inst_adc_hl_de,
    0x5B: inst_ld_de_nnm,
    0x62: inst_sbc_hl_hl,
    0x6A: inst_adc_hl_hl,
    0x72: inst_sbc_hl_sp,
    0x73: inst_ld_nnm_sp,
    0x7A: inst_adc_hl_sp,
    0x7B: inst_ld_sp_nnm,
    # Next register access
    0x91: inst_nextreg_nn,   # NEXTREG nn,mm
    0x92: inst_nextreg_a,    # NEXTREG nn,A
}

IX_INSTRUCTION_MAP = {  # 0xDD prefix (legacy; superseded by execute_index)
    0x21: inst_ld_ix_nn,
    0x66: inst_ld_h_ixm_disp,
    0x6E: inst_ld_l_ixm_disp,
    0xE9: inst_jp_ix,
}


# =====================================================================
# Complete base Z80 instruction set
# The blocks below are fully regular and are generated programmatically,
# then registered into INSTRUCTION_MAP. This guarantees coverage of every
# LD r,r', ALU A,r / A,n, INC/DEC r and LD r,n opcode, plus the CB and
# DD/FD prefix groups -- exactly as the real Z80 the binary was built for.
# =====================================================================

# 8-bit register selector: 0=B 1=C 2=D 3=E 4=H 5=L 6=(HL) 7=A
def _get_r(cpu, idx):
    if idx == 0:
        return cpu.B
    if idx == 1:
        return cpu.C
    if idx == 2:
        return cpu.D
    if idx == 3:
        return cpu.E
    if idx == 4:
        return cpu.H
    if idx == 5:
        return cpu.L
    if idx == 6:
        return cpu.mem[cpu.HL]
    return cpu.A


def _set_r(cpu, idx, v):
    v &= 0xFF
    if idx == 0:
        cpu.B = v
    elif idx == 1:
        cpu.C = v
    elif idx == 2:
        cpu.D = v
    elif idx == 3:
        cpu.E = v
    elif idx == 4:
        cpu.H = v
    elif idx == 5:
        cpu.L = v
    elif idx == 6:
        cpu.mem[cpu.HL] = v
    else:
        cpu.A = v


def _do_alu(cpu, group, b):
    """ALU group: 0 ADD 1 ADC 2 SUB 3 SBC 4 AND 5 XOR 6 OR 7 CP."""
    carry = 1 if (cpu.F & FLAG_C) else 0
    if group == 0:
        cpu.A = _add8(cpu, cpu.A, b)
    elif group == 1:
        cpu.A = _add8(cpu, cpu.A, b, carry)
    elif group == 2:
        cpu.A = _sub8(cpu, cpu.A, b)
    elif group == 3:
        cpu.A = _sub8(cpu, cpu.A, b, carry)
    elif group == 4:
        cpu.A = _logic8(cpu, cpu.A & b, True)
    elif group == 5:
        cpu.A = _logic8(cpu, cpu.A ^ b, False)
    elif group == 6:
        cpu.A = _logic8(cpu, cpu.A | b, False)
    else:
        _cp8(cpu, cpu.A, b)


def _disp(base, d):
    """Apply signed 8-bit displacement to a 16-bit base address."""
    if d & 0x80:
        d -= 0x100
    return (base + d) & 0xFFFF


def _gen_base_blocks():
    # LD r,r'  (0x40-0x7F, excluding 0x76 = HALT)
    for op in range(0x40, 0x80):
        if op == 0x76:
            continue
        dst = (op >> 3) & 7
        src = op & 7
        INSTRUCTION_MAP[op] = (lambda d, s: lambda cpu: _set_r(cpu, d, _get_r(cpu, s)))(dst, src)

    # ALU A,r  (0x80-0xBF)
    for op in range(0x80, 0xC0):
        grp = (op >> 3) & 7
        src = op & 7
        INSTRUCTION_MAP[op] = (lambda g, s: lambda cpu: _do_alu(cpu, g, _get_r(cpu, s)))(grp, src)

    # ALU A,n  (immediate)
    for op, grp in ((0xC6, 0), (0xCE, 1), (0xD6, 2), (0xDE, 3),
                    (0xE6, 4), (0xEE, 5), (0xF6, 6), (0xFE, 7)):
        INSTRUCTION_MAP[op] = (lambda g: lambda cpu: _do_alu(cpu, g, cpu.fetch_byte()))(grp)

    # INC r / DEC r  (0x04+8i / 0x05+8i)
    for idx in range(8):
        INSTRUCTION_MAP[0x04 + 8 * idx] = (lambda i: lambda cpu: _set_r(cpu, i, _inc8(cpu, _get_r(cpu, i))))(idx)
        INSTRUCTION_MAP[0x05 + 8 * idx] = (lambda i: lambda cpu: _set_r(cpu, i, _dec8(cpu, _get_r(cpu, i))))(idx)

    # LD r,n  (0x06+8i)
    for idx in range(8):
        INSTRUCTION_MAP[0x06 + 8 * idx] = (lambda i: lambda cpu: _set_r(cpu, i, cpu.fetch_byte()))(idx)


def _rlca(cpu):
    """0x07: RLCA"""
    c = (cpu.A >> 7) & 1
    cpu.A = ((cpu.A << 1) | c) & 0xFF
    cpu.F = (cpu.F & (FLAG_S | FLAG_Z | FLAG_PV)) | (cpu.A & (FLAG_5 | FLAG_3)) | (FLAG_C if c else 0)


def _rrca(cpu):
    """0x0F: RRCA"""
    c = cpu.A & 1
    cpu.A = ((cpu.A >> 1) | (c << 7)) & 0xFF
    cpu.F = (cpu.F & (FLAG_S | FLAG_Z | FLAG_PV)) | (cpu.A & (FLAG_5 | FLAG_3)) | (FLAG_C if c else 0)


def _rla(cpu):
    """0x17: RLA"""
    old = 1 if (cpu.F & FLAG_C) else 0
    c = (cpu.A >> 7) & 1
    cpu.A = ((cpu.A << 1) | old) & 0xFF
    cpu.F = (cpu.F & (FLAG_S | FLAG_Z | FLAG_PV)) | (cpu.A & (FLAG_5 | FLAG_3)) | (FLAG_C if c else 0)


def _rra(cpu):
    """0x1F: RRA"""
    old = 1 if (cpu.F & FLAG_C) else 0
    c = cpu.A & 1
    cpu.A = ((cpu.A >> 1) | (old << 7)) & 0xFF
    cpu.F = (cpu.F & (FLAG_S | FLAG_Z | FLAG_PV)) | (cpu.A & (FLAG_5 | FLAG_3)) | (FLAG_C if c else 0)


def _daa(cpu):
    """0x27: DAA - decimal adjust A."""
    a = cpu.A
    f = cpu.F
    corr = 0
    carry = 0
    if (f & FLAG_H) or (a & 0x0F) > 9:
        corr |= 0x06
    if (f & FLAG_C) or a > 0x99:
        corr |= 0x60
        carry = FLAG_C
    if f & FLAG_N:
        a = (a - corr) & 0xFF
        h = FLAG_H if ((cpu.A & 0x0F) < (corr & 0x0F)) else 0
    else:
        h = FLAG_H if ((cpu.A & 0x0F) + (corr & 0x0F)) & 0x10 else 0
        a = (a + corr) & 0xFF
    nf = f & FLAG_N
    cpu.A = a
    res = 0
    if a & 0x80:
        res |= FLAG_S
    if a == 0:
        res |= FLAG_Z
    res |= a & (FLAG_5 | FLAG_3)
    res |= h | nf | carry
    if _parity_even(a):
        res |= FLAG_PV
    cpu.F = res


def _cpl(cpu):
    """0x2F: CPL - A = ~A"""
    cpu.A = (~cpu.A) & 0xFF
    cpu.F = (cpu.F & (FLAG_S | FLAG_Z | FLAG_PV | FLAG_C)) | FLAG_H | FLAG_N | (cpu.A & (FLAG_5 | FLAG_3))


def _scf(cpu):
    """0x37: SCF - set carry"""
    cpu.F = (cpu.F & (FLAG_S | FLAG_Z | FLAG_PV)) | (cpu.A & (FLAG_5 | FLAG_3)) | FLAG_C


def _ccf(cpu):
    """0x3F: CCF - complement carry"""
    old = FLAG_H if (cpu.F & FLAG_C) else 0
    newc = 0 if (cpu.F & FLAG_C) else FLAG_C
    cpu.F = (cpu.F & (FLAG_S | FLAG_Z | FLAG_PV)) | (cpu.A & (FLAG_5 | FLAG_3)) | old | newc


def _ex_af(cpu):
    """0x08: EX AF,AF'"""
    cpu.A, cpu.A_alt = cpu.A_alt, cpu.A
    cpu.F, cpu.F_alt = cpu.F_alt, cpu.F


def _nop(cpu):
    pass


def _make_rst(vector):
    def f(cpu):
        cpu.push(cpu.PC)
        cpu.PC = vector
    return f


# --- Conditional JP/CALL/RET on parity (PO/PE) and sign (P/M) ---
# PO = parity odd  -> P/V clear; PE = parity even -> P/V set.
# P  = sign plus   -> S   clear; M  = sign minus  -> S   set.
# Used by inc/draw.f: `jpf po|` skips the EI when interrupts were disabled.

def _cond_po(cpu): return not (cpu.F & FLAG_PV)
def _cond_pe(cpu): return bool(cpu.F & FLAG_PV)
def _cond_p(cpu):  return not (cpu.F & FLAG_S)
def _cond_m(cpu):  return bool(cpu.F & FLAG_S)


def _make_jp_cc(cond):
    def f(cpu):
        lo = cpu.fetch_byte(); hi = cpu.fetch_byte()
        if cond(cpu):
            cpu.PC = lo | (hi << 8)
    return f


def _make_call_cc(cond):
    def f(cpu):
        lo = cpu.fetch_byte(); hi = cpu.fetch_byte()
        if cond(cpu):
            cpu.push(cpu.PC)
            cpu.PC = lo | (hi << 8)
    return f


def _make_ret_cc(cond):
    def f(cpu):
        if cond(cpu):
            cpu.PC = cpu.pop()
    return f


# --- Immediate-port I/O: IN A,(n) / OUT (n),A ---
# No hardware device is modelled by default. A host may install
# cpu.io_read(port)->int and/or cpu.io_write(port, val) to model real
# devices; absent those, reads see an idle bus (0xFF) and writes are dropped.

def _port_in(cpu, port):
    """Read an I/O port. Default 0xFF -- e.g. ULA port 0xFE then reports
    'no key pressed', which is what inc/^escape.f expects when [EDIT] is up."""
    hook = getattr(cpu, 'io_read', None)
    return (hook(port) & 0xFF) if hook is not None else 0xFF


def _port_out(cpu, port, val):
    """Write an I/O port. Discarded unless cpu.io_write(port, val) is set."""
    hook = getattr(cpu, 'io_write', None)
    if hook is not None:
        hook(port, val & 0xFF)


def inst_in_a_n(cpu):
    """0xDB n: IN A,(n) - A := port[(A<<8)|n]. Flags unaffected.

    Used by inc/^escape.f, which scans the ZX keyboard via ULA port 0xFE
    (e.g. `3E FE / DB FE` = LD A,$FE / IN A,($FE)).
    """
    n = cpu.fetch_byte()
    port = (cpu.A << 8) | n
    cpu.A = _port_in(cpu, port) & 0xFF


def inst_out_n_a(cpu):
    """0xD3 n: OUT (n),A - write A to port[(A<<8)|n]. Flags unaffected."""
    n = cpu.fetch_byte()
    port = (cpu.A << 8) | n
    _port_out(cpu, port, cpu.A)


def _register_misc():
    INSTRUCTION_MAP[0x07] = _rlca
    INSTRUCTION_MAP[0x0F] = _rrca
    INSTRUCTION_MAP[0x17] = _rla
    INSTRUCTION_MAP[0x1F] = _rra
    INSTRUCTION_MAP[0x27] = _daa
    INSTRUCTION_MAP[0x2F] = _cpl
    INSTRUCTION_MAP[0x37] = _scf
    INSTRUCTION_MAP[0x3F] = _ccf
    INSTRUCTION_MAP[0x08] = _ex_af
    INSTRUCTION_MAP[0x10] = inst_djnz  # DJNZ d (used by inc/ms.f)
    # Conditional JP/CALL/RET on parity (PO/PE) and sign (P/M).
    # JP PO is used by inc/draw.f.
    INSTRUCTION_MAP[0xE0] = _make_ret_cc(_cond_po)   # RET PO
    INSTRUCTION_MAP[0xE2] = _make_jp_cc(_cond_po)    # JP PO,nn
    INSTRUCTION_MAP[0xE4] = _make_call_cc(_cond_po)  # CALL PO,nn
    INSTRUCTION_MAP[0xE8] = _make_ret_cc(_cond_pe)   # RET PE
    INSTRUCTION_MAP[0xEA] = _make_jp_cc(_cond_pe)    # JP PE,nn
    INSTRUCTION_MAP[0xEC] = _make_call_cc(_cond_pe)  # CALL PE,nn
    INSTRUCTION_MAP[0xF0] = _make_ret_cc(_cond_p)    # RET P
    INSTRUCTION_MAP[0xF2] = _make_jp_cc(_cond_p)     # JP P,nn
    INSTRUCTION_MAP[0xF4] = _make_call_cc(_cond_p)   # CALL P,nn
    INSTRUCTION_MAP[0xF8] = _make_ret_cc(_cond_m)    # RET M
    INSTRUCTION_MAP[0xFA] = _make_jp_cc(_cond_m)     # JP M,nn
    INSTRUCTION_MAP[0xFC] = _make_call_cc(_cond_m)   # CALL M,nn
    INSTRUCTION_MAP[0xD3] = inst_out_n_a  # OUT (n),A
    INSTRUCTION_MAP[0xDB] = inst_in_a_n   # IN A,(n)  (used by inc/^escape.f)
    INSTRUCTION_MAP[0xF3] = _nop  # DI (interrupts not modelled)
    INSTRUCTION_MAP[0xFB] = _nop  # EI
    INSTRUCTION_MAP[0xF9] = lambda cpu: setattr(cpu, 'SP', cpu.HL)  # LD SP,HL
    INSTRUCTION_MAP[0xE3] = _ex_sp_hl    # EX (SP),HL
    INSTRUCTION_MAP[0xEB] = inst_ex_de_hl
    # RST vectors (0xCF / 0xD7 are intercepted by the emulator for I/O)
    for op, vec in ((0xC7, 0x00), (0xCF, 0x08), (0xD7, 0x10), (0xDF, 0x18),
                    (0xE7, 0x20), (0xEF, 0x28), (0xF7, 0x30), (0xFF, 0x38)):
        INSTRUCTION_MAP[op] = _make_rst(vec)


def _ex_sp_hl(cpu):
    """0xE3: EX (SP),HL"""
    top = cpu.mem16_le(cpu.SP)
    cpu.mem16_le_set(cpu.SP, cpu.HL)
    cpu.HL = top


def execute_cb(cpu):
    """0xCB prefix: rotates/shifts and BIT/RES/SET."""
    op = cpu.fetch_byte()
    reg = op & 7
    grp = op >> 6           # 0=rot/shift 1=BIT 2=RES 3=SET
    bit = (op >> 3) & 7
    val = _get_r(cpu, reg)

    if grp == 0:
        sub = (op >> 3) & 7  # 0 RLC 1 RRC 2 RL 3 RR 4 SLA 5 SRA 6 SLL 7 SRL
        cin = 1 if (cpu.F & FLAG_C) else 0
        if sub == 0:
            carry = (val >> 7) & 1
            val = ((val << 1) | carry) & 0xFF
        elif sub == 1:
            carry = val & 1
            val = ((val >> 1) | (carry << 7)) & 0xFF
        elif sub == 2:
            carry = (val >> 7) & 1
            val = ((val << 1) | cin) & 0xFF
        elif sub == 3:
            carry = val & 1
            val = ((val >> 1) | (cin << 7)) & 0xFF
        elif sub == 4:
            carry = (val >> 7) & 1
            val = (val << 1) & 0xFF
        elif sub == 5:
            carry = val & 1
            val = ((val >> 1) | (val & 0x80)) & 0xFF
        elif sub == 6:
            carry = (val >> 7) & 1
            val = ((val << 1) | 1) & 0xFF
        else:
            carry = val & 1
            val = (val >> 1) & 0xFF
        _set_r(cpu, reg, val)
        f = 0
        if val & 0x80:
            f |= FLAG_S
        if val == 0:
            f |= FLAG_Z
        f |= val & (FLAG_5 | FLAG_3)
        if _parity_even(val):
            f |= FLAG_PV
        if carry:
            f |= FLAG_C
        cpu.F = f
    elif grp == 1:  # BIT b,r
        zero = (val >> bit) & 1
        f = (cpu.F & FLAG_C) | FLAG_H
        if zero == 0:
            f |= FLAG_Z | FLAG_PV
        if bit == 7 and zero:
            f |= FLAG_S
        f |= val & (FLAG_5 | FLAG_3)
        cpu.F = f
    elif grp == 2:  # RES b,r
        _set_r(cpu, reg, val & ~(1 << bit))
    else:           # SET b,r
        _set_r(cpu, reg, val | (1 << bit))


def execute_index(cpu, name):
    """0xDD (IX) / 0xFD (IY) prefix decoder."""
    op = cpu.fetch_byte()
    ireg = getattr(cpu, name)

    if op in (0x09, 0x19, 0x29, 0x39):
        rr = {0x09: cpu.BC, 0x19: cpu.DE, 0x29: ireg, 0x39: cpu.SP}[op]
        setattr(cpu, name, _add16(cpu, ireg, rr))
        return
    if op == 0x21:
        lo = cpu.fetch_byte(); hi = cpu.fetch_byte()
        setattr(cpu, name, lo | (hi << 8)); return
    if op == 0x22:
        lo = cpu.fetch_byte(); hi = cpu.fetch_byte()
        cpu.mem16_le_set(lo | (hi << 8), ireg); return
    if op == 0x2A:
        lo = cpu.fetch_byte(); hi = cpu.fetch_byte()
        setattr(cpu, name, cpu.mem16_le(lo | (hi << 8))); return
    if op == 0x23:
        setattr(cpu, name, (ireg + 1) & 0xFFFF); return
    if op == 0x2B:
        setattr(cpu, name, (ireg - 1) & 0xFFFF); return
    if op == 0xE5:
        cpu.push(ireg); return
    if op == 0xE1:
        setattr(cpu, name, cpu.pop()); return
    if op == 0xE9:
        cpu.PC = ireg; return
    if op == 0xF9:
        cpu.SP = ireg; return
    if op == 0xE3:  # EX (SP),I
        top = cpu.mem16_le(cpu.SP)
        cpu.mem16_le_set(cpu.SP, ireg)
        setattr(cpu, name, top); return
    if op == 0x36:  # LD (I+d),n
        d = cpu.fetch_byte(); n = cpu.fetch_byte()
        cpu.mem[_disp(ireg, d)] = n & 0xFF; return
    if op == 0x34:  # INC (I+d)
        d = cpu.fetch_byte(); a = _disp(ireg, d)
        cpu.mem[a] = _inc8(cpu, cpu.mem[a]); return
    if op == 0x35:  # DEC (I+d)
        d = cpu.fetch_byte(); a = _disp(ireg, d)
        cpu.mem[a] = _dec8(cpu, cpu.mem[a]); return
    if op != 0x76 and (op & 0xC7) == 0x46:  # LD r,(I+d)  (0x46/4E/56/5E/66/6E/7E)
        d = cpu.fetch_byte(); a = _disp(ireg, d)
        _set_r(cpu, (op >> 3) & 7, cpu.mem[a]); return
    if 0x70 <= op <= 0x77 and op != 0x76:   # LD (I+d),r
        d = cpu.fetch_byte(); a = _disp(ireg, d)
        cpu.mem[a] = _get_r(cpu, op & 7); return
    if 0x80 <= op <= 0xBF and (op & 7) == 6:  # ALU A,(I+d)
        d = cpu.fetch_byte(); a = _disp(ireg, d)
        _do_alu(cpu, (op >> 3) & 7, cpu.mem[a]); return
    if op == 0xCB:  # DDCB d sub : bit ops on (I+d)
        d = cpu.fetch_byte(); sub = cpu.fetch_byte()
        _index_cb(cpu, _disp(ireg, d), sub); return

    # Unrecognised: the prefix acts as a no-op; execute the byte normally.
    if op in INSTRUCTION_MAP:
        INSTRUCTION_MAP[op](cpu)


def _index_cb(cpu, addr, sub):
    """DDCB/FDCB: rotate/shift or BIT/RES/SET on memory at (I+d)."""
    grp = sub >> 6
    bit = (sub >> 3) & 7
    val = cpu.mem[addr]
    if grp == 0:
        s = (sub >> 3) & 7
        cin = 1 if (cpu.F & FLAG_C) else 0
        if s == 0:
            carry = (val >> 7) & 1; val = ((val << 1) | carry) & 0xFF
        elif s == 1:
            carry = val & 1; val = ((val >> 1) | (carry << 7)) & 0xFF
        elif s == 2:
            carry = (val >> 7) & 1; val = ((val << 1) | cin) & 0xFF
        elif s == 3:
            carry = val & 1; val = ((val >> 1) | (cin << 7)) & 0xFF
        elif s == 4:
            carry = (val >> 7) & 1; val = (val << 1) & 0xFF
        elif s == 5:
            carry = val & 1; val = ((val >> 1) | (val & 0x80)) & 0xFF
        elif s == 6:
            carry = (val >> 7) & 1; val = ((val << 1) | 1) & 0xFF
        else:
            carry = val & 1; val = (val >> 1) & 0xFF
        cpu.mem[addr] = val
        f = 0
        if val & 0x80:
            f |= FLAG_S
        if val == 0:
            f |= FLAG_Z
        f |= val & (FLAG_5 | FLAG_3)
        if _parity_even(val):
            f |= FLAG_PV
        if carry:
            f |= FLAG_C
        cpu.F = f
    elif grp == 1:  # BIT
        zero = (val >> bit) & 1
        f = (cpu.F & FLAG_C) | FLAG_H
        if zero == 0:
            f |= FLAG_Z | FLAG_PV
        if bit == 7 and zero:
            f |= FLAG_S
        cpu.F = f
    elif grp == 2:
        cpu.mem[addr] = val & ~(1 << bit)
    else:
        cpu.mem[addr] = val | (1 << bit)


# --- Extended (ED) instructions used by the core but not yet mapped ---

def inst_neg(cpu):
    """0xED 0x44: NEG - A = 0 - A"""
    cpu.A = _sub8(cpu, 0, cpu.A)


def inst_ldir(cpu):
    """0xED 0xB0: LDIR - block copy (HL)->(DE), BC times, ascending."""
    while cpu.BC != 0:
        cpu.mem[cpu.DE] = cpu.mem[cpu.HL]
        cpu.HL = (cpu.HL + 1) & 0xFFFF
        cpu.DE = (cpu.DE + 1) & 0xFFFF
        cpu.BC = (cpu.BC - 1) & 0xFFFF
    cpu.F &= ~(FLAG_H | FLAG_PV | FLAG_N)


def inst_lddr(cpu):
    """0xED 0xB8: LDDR - block copy descending."""
    while cpu.BC != 0:
        cpu.mem[cpu.DE] = cpu.mem[cpu.HL]
        cpu.HL = (cpu.HL - 1) & 0xFFFF
        cpu.DE = (cpu.DE - 1) & 0xFFFF
        cpu.BC = (cpu.BC - 1) & 0xFFFF
    cpu.F &= ~(FLAG_H | FLAG_PV | FLAG_N)


def inst_ldi(cpu):
    """0xED 0xA0: LDI"""
    cpu.mem[cpu.DE] = cpu.mem[cpu.HL]
    cpu.HL = (cpu.HL + 1) & 0xFFFF
    cpu.DE = (cpu.DE + 1) & 0xFFFF
    cpu.BC = (cpu.BC - 1) & 0xFFFF
    cpu.F &= ~(FLAG_H | FLAG_N)
    if cpu.BC != 0:
        cpu.F |= FLAG_PV
    else:
        cpu.F &= ~FLAG_PV


def inst_in_a_c(cpu):
    """0xED 0x78: IN A,(C) - reads via _bc_port_in (NextReg read-back
    modelled). Note: _register_ed_standard() later remaps ED 78 to the
    flag-setting _make_in_r_c(7); both go through the same port model."""
    cpu.A = _bc_port_in(cpu)


def inst_out_c_a(cpu):
    """0xED 0x79: OUT (C),A - writes via _bc_port_out (NextReg select
    modelled). Also remapped by _register_ed_standard() to
    _make_out_c_r(7); both go through the same port model."""
    _bc_port_out(cpu, cpu.A)


def _register_extended():
    EXTENDED_MAP[0x44] = inst_neg
    EXTENDED_MAP[0xB0] = inst_ldir
    EXTENDED_MAP[0xB8] = inst_lddr
    EXTENDED_MAP[0xA0] = inst_ldi
    EXTENDED_MAP[0x78] = inst_in_a_c
    EXTENDED_MAP[0x79] = inst_out_c_a
    # LD (nn),rr / LD rr,(nn) for BC,DE,SP (HL forms are in the main map)
    EXTENDED_MAP[0x43] = _ld_nn_bc
    EXTENDED_MAP[0x4B] = _ld_bc_nn_mem
    EXTENDED_MAP[0x53] = _ld_nn_de
    # 0x5B (LD DE,(nn)) and 0x73/0x7B already present


def _ld_nn_bc(cpu):
    lo = cpu.fetch_byte(); hi = cpu.fetch_byte()
    cpu.mem16_le_set(lo | (hi << 8), cpu.BC)


def _ld_bc_nn_mem(cpu):
    lo = cpu.fetch_byte(); hi = cpu.fetch_byte()
    cpu.BC = cpu.mem16_le(lo | (hi << 8))


def _ld_nn_de(cpu):
    lo = cpu.fetch_byte(); hi = cpu.fetch_byte()
    cpu.mem16_le_set(lo | (hi << 8), cpu.DE)


# =====================================================================
# Z80N extensions that were previously missing (vs the official
# https://wiki.specnext.dev/Extended_Z80_instruction_set table).
# All Z80N ALU/shift extensions leave the flags UNAFFECTED, except
# TEST which sets flags exactly as "AND n" (A itself stays unchanged).
# =====================================================================

def inst_swapnib(cpu):
    """0xED 0x23: SWAPNIB - swap the two nibbles of A. Flags unaffected."""
    a = cpu.A & 0xFF
    cpu.A = ((a << 4) | (a >> 4)) & 0xFF


def inst_mirror_a(cpu):
    """0xED 0x24: MIRROR A - reverse the bit order of A (bit0<->bit7...)."""
    a = cpu.A & 0xFF
    r = 0
    for _ in range(8):
        r = (r << 1) | (a & 1)
        a >>= 1
    cpu.A = r & 0xFF


def inst_test_n(cpu):
    """0xED 0x27 n: TEST n - set flags as for AND n, but A is unchanged."""
    n = cpu.fetch_byte()
    _logic8(cpu, cpu.A & n, True)  # sets cpu.F (H=1,C=0,N=0,PV=parity); A untouched


def inst_bsra_de_b(cpu):
    """0xED 0x29: BSRA DE,B - barrel arithmetic shift right (sign-preserving)."""
    n = cpu.B & 0x1F
    de = cpu.DE
    sign = de & 0x8000
    if n >= 16:
        cpu.DE = 0xFFFF if sign else 0
    else:
        res = de >> n
        if sign:
            res |= (0xFFFF << (16 - n)) & 0xFFFF
        cpu.DE = res & 0xFFFF


def inst_bsrf_de_b(cpu):
    """0xED 0x2B: BSRF DE,B - barrel shift right filling vacated bits with 1s."""
    n = cpu.B & 0x1F
    de = cpu.DE
    if n >= 16:
        cpu.DE = 0xFFFF
    else:
        cpu.DE = ((de >> n) | ((0xFFFF << (16 - n)) & 0xFFFF)) & 0xFFFF


def inst_brlc_de_b(cpu):
    """0xED 0x2C: BRLC DE,B - barrel rotate left DE by (B & 0x0F) bits."""
    n = cpu.B & 0x0F
    de = cpu.DE
    cpu.DE = ((de << n) | (de >> (16 - n))) & 0xFFFF if n else de


def inst_outinb(cpu):
    """0xED 0x90: OUTINB - like OUTI but B is NOT decremented.

    OUT (BC),(HL); HL++. No I/O device modelled, so the write is discarded.
    """
    cpu.HL = (cpu.HL + 1) & 0xFFFF


def inst_pixeldn(cpu):
    """0xED 0x93: PIXELDN - advance HL (a ULA pixel address) one scan-line down."""
    hl = cpu.HL
    if (hl & 0x0700) != 0x0700:
        hl = (hl + 0x0100) & 0xFFFF
    else:
        hl &= 0xF8FF
        if (hl & 0x00E0) != 0x00E0:
            hl = (hl + 0x0020) & 0xFFFF
        else:
            hl &= 0xFF1F
            hl = (hl + 0x0800) & 0xFFFF
    cpu.HL = hl


def inst_pixelad(cpu):
    """0xED 0x94: PIXELAD - HL := ULA pixel byte address for Y=D, X=E."""
    y = cpu.D & 0xFF
    x = cpu.E & 0xFF
    cpu.HL = (0x4000
              | ((y & 0xC0) << 5)
              | ((y & 0x07) << 8)
              | ((y & 0x38) << 2)
              | (x >> 3)) & 0xFFFF


def inst_setae(cpu):
    """0xED 0x95: SETAE - A := the one-bit pixel mask within a byte for X=E."""
    cpu.A = (0x80 >> (cpu.E & 7)) & 0xFF


def inst_jp_c_port(cpu):
    """0xED 0x98: JP (C) - IN (C), then jump within the current 64-byte block.

    With no I/O device modelled, IN (C) yields 0xFF, so the low 6 bits of PC
    become 0x3F. Documented behaviour; effectively inert without real I/O.
    """
    read = 0xFF  # IN (C) with no device
    cpu.PC = (cpu.PC & 0xFFC0) | (read & 0x3F)


# --- Z80N extended block-copy with A-transparency ---

def inst_ldix(cpu):
    """0xED 0xA4: LDIX - LDI variant; byte equal to A is treated as transparent.

    temp=(HL); if temp!=A: (DE)=temp; DE++; HL++; BC--.
    """
    temp = cpu.mem[cpu.HL]
    if temp != (cpu.A & 0xFF):
        cpu.mem[cpu.DE] = temp
    cpu.DE = (cpu.DE + 1) & 0xFFFF
    cpu.HL = (cpu.HL + 1) & 0xFFFF
    cpu.BC = (cpu.BC - 1) & 0xFFFF


def inst_lddx(cpu):
    """0xED 0xAC: LDDX - like LDIX but HL decrements (DE still increments)."""
    temp = cpu.mem[cpu.HL]
    if temp != (cpu.A & 0xFF):
        cpu.mem[cpu.DE] = temp
    cpu.DE = (cpu.DE + 1) & 0xFFFF
    cpu.HL = (cpu.HL - 1) & 0xFFFF
    cpu.BC = (cpu.BC - 1) & 0xFFFF


def inst_ldirx(cpu):
    """0xED 0xB4: LDIRX - repeat LDIX until BC == 0."""
    a = cpu.A & 0xFF
    while True:
        temp = cpu.mem[cpu.HL]
        if temp != a:
            cpu.mem[cpu.DE] = temp
        cpu.DE = (cpu.DE + 1) & 0xFFFF
        cpu.HL = (cpu.HL + 1) & 0xFFFF
        cpu.BC = (cpu.BC - 1) & 0xFFFF
        if cpu.BC == 0:
            break


def inst_lddrx(cpu):
    """0xED 0xBC: LDDRX - repeat LDDX (HL descending) until BC == 0."""
    a = cpu.A & 0xFF
    while True:
        temp = cpu.mem[cpu.HL]
        if temp != a:
            cpu.mem[cpu.DE] = temp
        cpu.DE = (cpu.DE + 1) & 0xFFFF
        cpu.HL = (cpu.HL - 1) & 0xFFFF
        cpu.BC = (cpu.BC - 1) & 0xFFFF
        if cpu.BC == 0:
            break


def inst_ldpirx(cpu):
    """0xED 0xB7: LDPIRX - pattern fill from an 8-byte table based at HL&0xFFF8.

    Each step the source byte is at (HL & 0xFFF8) | (E & 7); HL stays fixed.
    Byte equal to A is transparent. DE++, BC-- until BC == 0.
    """
    a = cpu.A & 0xFF
    while True:
        src = (cpu.HL & 0xFFF8) | (cpu.E & 0x07)
        temp = cpu.mem[src]
        if temp != a:
            cpu.mem[cpu.DE] = temp
        cpu.DE = (cpu.DE + 1) & 0xFFFF
        cpu.BC = (cpu.BC - 1) & 0xFFFF
        if cpu.BC == 0:
            break


def inst_ldws(cpu):
    """0xED 0xA5: LDWS - (DE)=(HL); INC L (no carry to H); INC D (sets flags)."""
    cpu.mem[cpu.DE] = cpu.mem[cpu.HL]
    cpu.L = (cpu.L + 1) & 0xFF
    cpu.D = _inc8(cpu, cpu.D)


def _register_z80n_ext():
    EXTENDED_MAP[0x23] = inst_swapnib
    EXTENDED_MAP[0x24] = inst_mirror_a
    EXTENDED_MAP[0x27] = inst_test_n
    EXTENDED_MAP[0x29] = inst_bsra_de_b
    EXTENDED_MAP[0x2B] = inst_bsrf_de_b
    EXTENDED_MAP[0x2C] = inst_brlc_de_b
    EXTENDED_MAP[0x90] = inst_outinb
    EXTENDED_MAP[0x93] = inst_pixeldn
    EXTENDED_MAP[0x94] = inst_pixelad
    EXTENDED_MAP[0x95] = inst_setae
    EXTENDED_MAP[0x98] = inst_jp_c_port
    EXTENDED_MAP[0xA4] = inst_ldix
    EXTENDED_MAP[0xA5] = inst_ldws
    EXTENDED_MAP[0xAC] = inst_lddx
    EXTENDED_MAP[0xB4] = inst_ldirx
    EXTENDED_MAP[0xB7] = inst_ldpirx
    EXTENDED_MAP[0xBC] = inst_lddrx


# =====================================================================
# Standard Z80 ED-prefixed instructions that were previously missing.
# =====================================================================

def inst_ldd(cpu):
    """0xED 0xA8: LDD - (DE)=(HL); HL--; DE--; BC--. H=0,N=0; PV=(BC!=0)."""
    val = cpu.mem[cpu.HL]
    cpu.mem[cpu.DE] = val
    cpu.HL = (cpu.HL - 1) & 0xFFFF
    cpu.DE = (cpu.DE - 1) & 0xFFFF
    cpu.BC = (cpu.BC - 1) & 0xFFFF
    f = cpu.F & (FLAG_S | FLAG_Z | FLAG_C)
    if cpu.BC != 0:
        f |= FLAG_PV
    n = (cpu.A + val) & 0xFF
    f |= n & FLAG_3
    f |= (n << 4) & FLAG_5  # bit 1 of (A+val) -> F5
    cpu.F = f


def _cp_block(cpu, val):
    """Common CPI/CPD flag computation (result of A - val, not stored)."""
    carry = cpu.F & FLAG_C
    res = (cpu.A - val) & 0xFF
    half = FLAG_H if ((cpu.A & 0x0F) - (val & 0x0F)) & 0x10 else 0
    f = FLAG_N | carry | half
    if res & 0x80:
        f |= FLAG_S
    if res == 0:
        f |= FLAG_Z
    if cpu.BC != 0:
        f |= FLAG_PV
    n = (res - (1 if half else 0)) & 0xFF
    f |= n & FLAG_3
    f |= (n << 4) & FLAG_5  # bit 1 of n -> F5
    cpu.F = f


def inst_cpi(cpu):
    """0xED 0xA1: CPI - compare A with (HL); HL++; BC--."""
    val = cpu.mem[cpu.HL]
    cpu.HL = (cpu.HL + 1) & 0xFFFF
    cpu.BC = (cpu.BC - 1) & 0xFFFF
    _cp_block(cpu, val)


def inst_cpd(cpu):
    """0xED 0xA9: CPD - compare A with (HL); HL--; BC--."""
    val = cpu.mem[cpu.HL]
    cpu.HL = (cpu.HL - 1) & 0xFFFF
    cpu.BC = (cpu.BC - 1) & 0xFFFF
    _cp_block(cpu, val)


def inst_cpir(cpu):
    """0xED 0xB1: CPIR - repeat CPI until BC==0 or a match (Z set)."""
    while True:
        inst_cpi(cpu)
        if cpu.BC == 0 or (cpu.F & FLAG_Z):
            break


def inst_cpdr(cpu):
    """0xED 0xB9: CPDR - repeat CPD until BC==0 or a match (Z set)."""
    while True:
        inst_cpd(cpu)
        if cpu.BC == 0 or (cpu.F & FLAG_Z):
            break


def _rrd_rld_flags(cpu):
    """S,Z,PV(parity),F3,F5 from A; H=0,N=0; C preserved."""
    a = cpu.A & 0xFF
    f = cpu.F & FLAG_C
    if a & 0x80:
        f |= FLAG_S
    if a == 0:
        f |= FLAG_Z
    f |= a & (FLAG_5 | FLAG_3)
    if _parity_even(a):
        f |= FLAG_PV
    cpu.F = f


def inst_rrd(cpu):
    """0xED 0x67: RRD - rotate nibbles right between A and (HL)."""
    val = cpu.mem[cpu.HL]
    cpu.mem[cpu.HL] = (((cpu.A & 0x0F) << 4) | (val >> 4)) & 0xFF
    cpu.A = (cpu.A & 0xF0) | (val & 0x0F)
    _rrd_rld_flags(cpu)


def inst_rld(cpu):
    """0xED 0x6F: RLD - rotate nibbles left between A and (HL)."""
    val = cpu.mem[cpu.HL]
    cpu.mem[cpu.HL] = (((val << 4) | (cpu.A & 0x0F))) & 0xFF
    cpu.A = (cpu.A & 0xF0) | (val >> 4)
    _rrd_rld_flags(cpu)


def inst_ld_a_i(cpu):
    """0xED 0x57: LD A,I - A=I; S,Z from I; H=0,N=0; PV=IFF2; C preserved."""
    i = getattr(cpu, 'I', 0) & 0xFF
    cpu.A = i
    f = cpu.F & FLAG_C
    if i & 0x80:
        f |= FLAG_S
    if i == 0:
        f |= FLAG_Z
    f |= i & (FLAG_5 | FLAG_3)
    if getattr(cpu, 'IFF2', 0):
        f |= FLAG_PV
    cpu.F = f


def inst_ld_a_r(cpu):
    """0xED 0x5F: LD A,R - A=R; flags as LD A,I (PV=IFF2)."""
    r = getattr(cpu, 'R', 0) & 0xFF
    cpu.A = r
    f = cpu.F & FLAG_C
    if r & 0x80:
        f |= FLAG_S
    if r == 0:
        f |= FLAG_Z
    f |= r & (FLAG_5 | FLAG_3)
    if getattr(cpu, 'IFF2', 0):
        f |= FLAG_PV
    cpu.F = f


def inst_ld_i_a(cpu):
    """0xED 0x47: LD I,A - I=A. No flags affected."""
    cpu.I = cpu.A & 0xFF


def inst_ld_r_a(cpu):
    """0xED 0x4F: LD R,A - R=A. No flags affected."""
    cpu.R = cpu.A & 0xFF


def _bc_port_in(cpu):
    """Read the 16-bit port in BC. The only device modelled is the NextReg
    read-back pair $243B/$253B: the core's MMU7_read selects register 87 on
    $243B and reads its value back on $253B. Since the (EMITC) fix it runs
    on every emitted character, so it must see the real tracked MMU7 page
    (a dummy $FF would then be written back through `nextreg 87,a` and swap
    garbage into $E000-$FFFF). Anything else reads an idle bus (0xFF)."""
    if cpu.BC == 0x253B and getattr(cpu, 'nextreg_selected', None) == 87:
        return cpu.mmu7_page & 0xFF
    return 0xFF


def _bc_port_out(cpu, val):
    """Write the 16-bit port in BC; models the NextReg select port $243B."""
    if cpu.BC == 0x243B:
        cpu.nextreg_selected = val & 0xFF


def _make_in_r_c(idx):
    """IN r,(C): reads via _bc_port_in (NextReg read-back modelled);
    set S,Z,P,F3,F5; H=0,N=0."""
    def f(cpu):
        val = _bc_port_in(cpu)
        if idx != 6:        # idx 6 = "IN (C)" : flags only, no register write
            _set_r(cpu, idx, val)
        flags = cpu.F & FLAG_C
        if val & 0x80:
            flags |= FLAG_S
        if val == 0:
            flags |= FLAG_Z
        flags |= val & (FLAG_5 | FLAG_3)
        if _parity_even(val):
            flags |= FLAG_PV
        cpu.F = flags
    return f


def _make_out_c_r(idx):
    """OUT (C),r: writes via _bc_port_out (NextReg select modelled);
    other ports discard. (idx 6 = OUT (C),0.)"""
    def f(cpu):
        _bc_port_out(cpu, 0 if idx == 6 else _get_r(cpu, idx))
    return f


def _make_block_io(name, hl_step, repeat):
    """INI/IND/INIR/INDR/OUTI/OUTD/OTIR/OTDR -- functional, no real device.

    IN ports read 0xFF; OUT ports discard. B decremented, HL stepped.
    Flags are approximated: Z set when B reaches 0, N=1.
    """
    is_in = name.startswith('IN')

    def step(cpu):
        if is_in:
            cpu.mem[cpu.HL] = 0xFF  # IN (C) -> (HL)
        # else OUT (C),(HL): value discarded
        cpu.B = (cpu.B - 1) & 0xFF
        cpu.HL = (cpu.HL + hl_step) & 0xFFFF
        f = FLAG_N
        if cpu.B == 0:
            f |= FLAG_Z
        if cpu.B & 0x80:
            f |= FLAG_S
        cpu.F = (cpu.F & FLAG_C) | f

    if not repeat:
        return step

    def loop(cpu):
        while True:
            step(cpu)
            if cpu.B == 0:
                break
    return loop


def inst_reti_retn(cpu):
    """0xED 0x4D RETI / 0xED 0x45 RETN - return; behaves like RET here."""
    cpu.PC = cpu.pop()


def _im_noop(cpu):
    """IM 0/1/2 - interrupt mode select; not modelled (no-op)."""
    pass


def _register_ed_standard():
    EXTENDED_MAP[0xA8] = inst_ldd
    EXTENDED_MAP[0xA1] = inst_cpi
    EXTENDED_MAP[0xA9] = inst_cpd
    EXTENDED_MAP[0xB1] = inst_cpir
    EXTENDED_MAP[0xB9] = inst_cpdr
    EXTENDED_MAP[0x67] = inst_rrd
    EXTENDED_MAP[0x6F] = inst_rld
    EXTENDED_MAP[0x57] = inst_ld_a_i
    EXTENDED_MAP[0x5F] = inst_ld_a_r
    EXTENDED_MAP[0x47] = inst_ld_i_a
    EXTENDED_MAP[0x4F] = inst_ld_r_a
    # RETN / RETI (and the undocumented duplicates of RETN)
    for op in (0x45, 0x4D, 0x55, 0x5D, 0x65, 0x6D, 0x75, 0x7D):
        EXTENDED_MAP[op] = inst_reti_retn
    # NEG and its undocumented duplicates
    for op in (0x44, 0x4C, 0x54, 0x5C, 0x64, 0x6C, 0x74, 0x7C):
        EXTENDED_MAP[op] = inst_neg
    # IM 0/1/2 (and undocumented duplicates)
    for op in (0x46, 0x4E, 0x56, 0x5E, 0x66, 0x6E, 0x76, 0x7E):
        EXTENDED_MAP[op] = _im_noop
    # IN r,(C) : ED 40/48/50/58/60/68/70(flags only)/78
    for idx, op in enumerate(range(0x40, 0x79, 8)):
        EXTENDED_MAP[op] = _make_in_r_c(idx)
    # OUT (C),r : ED 41/49/51/59/61/69/71(out 0)/79
    for idx, op in enumerate(range(0x41, 0x7A, 8)):
        EXTENDED_MAP[op] = _make_out_c_r(idx)
    # Block I/O
    EXTENDED_MAP[0xA2] = _make_block_io('INI', +1, False)
    EXTENDED_MAP[0xAA] = _make_block_io('IND', -1, False)
    EXTENDED_MAP[0xB2] = _make_block_io('INIR', +1, True)
    EXTENDED_MAP[0xBA] = _make_block_io('INDR', -1, True)
    EXTENDED_MAP[0xA3] = _make_block_io('OUTI', +1, False)
    EXTENDED_MAP[0xAB] = _make_block_io('OUTD', -1, False)
    EXTENDED_MAP[0xB3] = _make_block_io('OTIR', +1, True)
    EXTENDED_MAP[0xBB] = _make_block_io('OTDR', -1, True)


# Populate the maps with the generated/complete instruction set.
_gen_base_blocks()
_register_misc()
_register_extended()
_register_z80n_ext()
_register_ed_standard()
