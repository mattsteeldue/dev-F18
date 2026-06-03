"""
Z80/Z80N instruction implementation for vForth emulator
Instruction reference: Z80 User Manual, Z80N extensions
"""


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
    cpu.A = (cpu.A + 1) & 0xFF


def inst_dec_a(cpu):
    """0x3D: DEC A - decrement A"""
    cpu.A = (cpu.A - 1) & 0xFF


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
    """0x76: HALT - halt processor"""
    cpu.halted = True
    raise StopIteration()


def inst_or_a(cpu):
    """0xB7: OR A - OR A with itself (test if zero)"""
    cpu.A = cpu.A | cpu.A
    # Set flags (simplified)


def inst_cp_a(cpu):
    """0xBF: CP A - compare A with itself (always equal)"""
    # Sets flags: Z=1, N=1, others affected by subtraction


def inst_xor_a(cpu):
    """0xAF: XOR A - XOR A with itself (clear A)"""
    cpu.A = 0


def inst_and_a(cpu):
    """0xA7: AND A - AND A with itself (no change)"""
    pass


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
    cpu.B = (cpu.B + 1) & 0xFF


def inst_inc_c(cpu):
    """0x0C: INC C - increment C"""
    cpu.C = (cpu.C + 1) & 0xFF


def inst_inc_d(cpu):
    """0x14: INC D - increment D"""
    cpu.D = (cpu.D + 1) & 0xFF


def inst_inc_e(cpu):
    """0x1C: INC E - increment E"""
    cpu.E = (cpu.E + 1) & 0xFF


def inst_inc_h(cpu):
    """0x24: INC H - increment H"""
    cpu.H = (cpu.H + 1) & 0xFF


def inst_inc_l(cpu):
    """0x2C: INC L - increment L"""
    cpu.L = (cpu.L + 1) & 0xFF


def inst_inc_hlm(cpu):
    """0x34: INC (HL) - increment memory at HL"""
    val = (cpu.mem[cpu.HL] + 1) & 0xFF
    cpu.mem[cpu.HL] = val


def inst_dec_b(cpu):
    """0x05: DEC B - decrement B"""
    cpu.B = (cpu.B - 1) & 0xFF


def inst_dec_c(cpu):
    """0x0D: DEC C - decrement C"""
    cpu.C = (cpu.C - 1) & 0xFF


def inst_dec_d(cpu):
    """0x15: DEC D - decrement D"""
    cpu.D = (cpu.D - 1) & 0xFF


def inst_dec_e(cpu):
    """0x1D: DEC E - decrement E"""
    cpu.E = (cpu.E - 1) & 0xFF


def inst_dec_h(cpu):
    """0x25: DEC H - decrement H"""
    cpu.H = (cpu.H - 1) & 0xFF


def inst_dec_l(cpu):
    """0x2D: DEC L - decrement L"""
    cpu.L = (cpu.L - 1) & 0xFF


def inst_dec_hlm(cpu):
    """0x35: DEC (HL) - decrement memory at HL"""
    val = (cpu.mem[cpu.HL] - 1) & 0xFF
    cpu.mem[cpu.HL] = val


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
    """0xCD nn: CALL nn - call subroutine at nn"""
    lo = cpu.fetch_byte()
    hi = cpu.fetch_byte()
    addr = lo | (hi << 8)
    # vForth uses DE as return stack (RP), not SP
    cpu.DE = (cpu.DE - 2) & 0xFFFF
    cpu.mem16_le_set(cpu.DE, cpu.PC)
    cpu.PC = addr


def inst_ret(cpu):
    """0xC9: RET - EXIT from high-level definition (matches vForth EXIT in L0.asm)"""
    # In vForth direct threading, RET executes EXIT:
    # 1. Pop IP (BC) from vForth return stack (DE)
    # 2. Update DE (return stack pointer)
    # 3. Jump to Next_Ptr (IX) to continue interpretation
    # This exactly matches the Z80 code in L0.asm lines 1402-1411
    cpu.BC = cpu.mem16_le(cpu.DE)
    cpu.DE = (cpu.DE + 2) & 0xFFFF
    # The actual jump to IX is handled by the emulator setting PC = IX
    # (This will be done in the dispatch loop after RET returns)
    # Jump to Next_Ptr is handled by the emulator's dispatch recognizing this as native


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
    result = (cpu.A + cpu.B) & 0xFF
    cpu.A = result


def inst_add_a_c(cpu):
    """0x81: ADD A,C - add C to A"""
    result = (cpu.A + cpu.C) & 0xFF
    cpu.A = result


def inst_add_a_d(cpu):
    """0x82: ADD A,D - add D to A"""
    result = (cpu.A + cpu.D) & 0xFF
    cpu.A = result


def inst_add_a_e(cpu):
    """0x83: ADD A,E - add E to A"""
    result = (cpu.A + cpu.E) & 0xFF
    cpu.A = result


def inst_sub_a_b(cpu):
    """0x90: SUB A,B - subtract B from A"""
    result = (cpu.A - cpu.B) & 0xFF
    cpu.A = result


def inst_sub_a_c(cpu):
    """0x91: SUB A,C - subtract C from A"""
    result = (cpu.A - cpu.C) & 0xFF
    cpu.A = result


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
        disp = -(~disp & 0xFF)
    if cpu.F & 0x01:  # C flag set
        cpu.PC = (cpu.PC + disp) & 0xFFFF


def inst_jr_nc_n(cpu):
    """0x30 n: JR NC,n - jump relative if no carry"""
    disp = cpu.fetch_byte()
    if disp & 0x80:
        disp = -(~disp & 0xFF)
    if not (cpu.F & 0x01):  # C flag not set
        cpu.PC = (cpu.PC + disp) & 0xFFFF


def inst_jr_z_n(cpu):
    """0x28 n: JR Z,n - jump relative if zero"""
    disp = cpu.fetch_byte()
    if disp & 0x80:
        disp = -(~disp & 0xFF)
    if cpu.F & 0x40:  # Z flag set
        cpu.PC = (cpu.PC + disp) & 0xFFFF


def inst_jr_nz_n(cpu):
    """0x20 n: JR NZ,n - jump relative if not zero"""
    disp = cpu.fetch_byte()
    if disp & 0x80:
        disp = -(~disp & 0xFF)
    if not (cpu.F & 0x40):  # Z flag not set
        cpu.PC = (cpu.PC + disp) & 0xFFFF


def inst_jr_n(cpu):
    """0x18 n: JR n - jump relative"""
    disp = cpu.fetch_byte()
    if disp & 0x80:
        disp = -(~disp & 0xFF)
    cpu.PC = (cpu.PC + disp) & 0xFFFF


def inst_ld_hl_nnm(cpu):
    """0x2A nn: LD HL,(nn) - load HL from memory at nn"""
    lo = cpu.fetch_byte()
    hi = cpu.fetch_byte()
    addr = lo | (hi << 8)
    cpu.HL = cpu.mem16_le(addr)


def inst_ld_bc_nnm(cpu):
    """0x0A nn: LD BC,(nn) - load BC from memory at nn"""
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
    """0x03 nn: LD (nn),BC - store BC into memory at nn"""
    lo = cpu.fetch_byte()
    hi = cpu.fetch_byte()
    addr = lo | (hi << 8)
    cpu.mem16_le_set(addr, cpu.BC)


def inst_sub_a_h(cpu):
    """0x94: SUB A,H - subtract H from A"""
    result = (cpu.A - cpu.H) & 0xFF
    cpu.A = result


def inst_sub_a_l(cpu):
    """0x95: SUB A,L - subtract L from A"""
    result = (cpu.A - cpu.L) & 0xFF
    cpu.A = result


def inst_sub_a_hlm(cpu):
    """0x96: SUB A,(HL) - subtract memory at HL from A"""
    result = (cpu.A - cpu.mem[cpu.HL]) & 0xFF
    cpu.A = result


def inst_sub_a_nn(cpu):
    """0xD6 n: SUB A,n - subtract immediate from A"""
    val = cpu.fetch_byte()
    result = (cpu.A - val) & 0xFF
    cpu.A = result


def inst_add_a_h(cpu):
    """0x84: ADD A,H - add H to A"""
    result = (cpu.A + cpu.H) & 0xFF
    cpu.A = result


def inst_add_a_l(cpu):
    """0x85: ADD A,L - add L to A"""
    result = (cpu.A + cpu.L) & 0xFF
    cpu.A = result


def inst_add_a_hlm(cpu):
    """0x86: ADD A,(HL) - add memory at HL to A"""
    result = (cpu.A + cpu.mem[cpu.HL]) & 0xFF
    cpu.A = result


def inst_add_a_nn(cpu):
    """0xC6 n: ADD A,n - add immediate to A"""
    val = cpu.fetch_byte()
    result = (cpu.A + val) & 0xFF
    cpu.A = result


def inst_cp_nn(cpu):
    """0xFE n: CP n - compare A with immediate"""
    val = cpu.fetch_byte()
    # Sets flags (Z if equal, etc.) but doesn't modify A


def inst_cp_hlm(cpu):
    """0xBE: CP (HL) - compare A with memory at HL"""
    # Sets flags (Z if equal, etc.) but doesn't modify A


def inst_and_nn(cpu):
    """0xE6 n: AND A,n - AND A with immediate"""
    val = cpu.fetch_byte()
    cpu.A = cpu.A & val


def inst_or_nn(cpu):
    """0xF6 n: OR A,n - OR A with immediate"""
    val = cpu.fetch_byte()
    cpu.A = cpu.A | val


def inst_xor_nn(cpu):
    """0xEE n: XOR A,n - XOR A with immediate"""
    val = cpu.fetch_byte()
    cpu.A = cpu.A ^ val


def inst_ld_hl_de_a(cpu):
    """0xED 0x31 nn: LDDR-style instruction placeholder"""
    # Skip operands for now
    cpu.fetch_byte()
    cpu.fetch_byte()


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
    cpu.HL = (cpu.HL + cpu.BC) & 0xFFFF


def inst_add_hl_de(cpu):
    """0x19: ADD HL,DE - add DE to HL"""
    cpu.HL = (cpu.HL + cpu.DE) & 0xFFFF


def inst_add_hl_hl(cpu):
    """0x29: ADD HL,HL - add HL to HL (shift left)"""
    cpu.HL = (cpu.HL + cpu.HL) & 0xFFFF


def inst_add_hl_sp(cpu):
    """0x39: ADD HL,SP - add SP to HL"""
    cpu.HL = (cpu.HL + cpu.SP) & 0xFFFF


def inst_or_a_b(cpu):
    """0xB0: OR A,B - OR A with B"""
    cpu.A = cpu.A | cpu.B


def inst_or_a_c(cpu):
    """0xB1: OR A,C - OR A with C"""
    cpu.A = cpu.A | cpu.C


def inst_or_a_d(cpu):
    """0xB2: OR A,D - OR A with D"""
    cpu.A = cpu.A | cpu.D


def inst_or_a_e(cpu):
    """0xB3: OR A,E - OR A with E"""
    cpu.A = cpu.A | cpu.E


def inst_or_a_h(cpu):
    """0xB4: OR A,H - OR A with H"""
    cpu.A = cpu.A | cpu.H


def inst_or_a_l(cpu):
    """0xB5: OR A,L - OR A with L"""
    cpu.A = cpu.A | cpu.L


def inst_or_a_hlm(cpu):
    """0xB6: OR A,(HL) - OR A with memory at HL"""
    cpu.A = cpu.A | cpu.mem[cpu.HL]


def inst_and_a_b(cpu):
    """0xA0: AND A,B - AND A with B"""
    cpu.A = cpu.A & cpu.B


def inst_and_a_c(cpu):
    """0xA1: AND A,C - AND A with C"""
    cpu.A = cpu.A & cpu.C


def inst_and_a_d(cpu):
    """0xA2: AND A,D - AND A with D"""
    cpu.A = cpu.A & cpu.D


def inst_and_a_e(cpu):
    """0xA3: AND A,E - AND A with E"""
    cpu.A = cpu.A & cpu.E


def inst_and_a_h(cpu):
    """0xA4: AND A,H - AND A with H"""
    cpu.A = cpu.A & cpu.H


def inst_and_a_l(cpu):
    """0xA5: AND A,L - AND A with L"""
    cpu.A = cpu.A & cpu.L


def inst_and_a_hlm(cpu):
    """0xA6: AND A,(HL) - AND A with memory at HL"""
    cpu.A = cpu.A & cpu.mem[cpu.HL]


def inst_xor_a_b(cpu):
    """0xA8: XOR A,B - XOR A with B"""
    cpu.A = cpu.A ^ cpu.B


def inst_xor_a_c(cpu):
    """0xA9: XOR A,C - XOR A with C"""
    cpu.A = cpu.A ^ cpu.C


def inst_xor_a_d(cpu):
    """0xAA: XOR A,D - XOR A with D"""
    cpu.A = cpu.A ^ cpu.D


def inst_xor_a_e(cpu):
    """0xAB: XOR A,E - XOR A with E"""
    cpu.A = cpu.A ^ cpu.E


def inst_xor_a_h(cpu):
    """0xAC: XOR A,H - XOR A with H"""
    cpu.A = cpu.A ^ cpu.H


def inst_xor_a_l(cpu):
    """0xAD: XOR A,L - XOR A with L"""
    cpu.A = cpu.A ^ cpu.L


def inst_xor_a_hlm(cpu):
    """0xAE: XOR A,(HL) - XOR A with memory at HL"""
    cpu.A = cpu.A ^ cpu.mem[cpu.HL]


def inst_cp_a_b(cpu):
    """0xB8: CP A,B - compare A with B"""
    pass


def inst_cp_a_c(cpu):
    """0xB9: CP A,C - compare A with C"""
    pass


def inst_cp_a_d(cpu):
    """0xBA: CP A,D - compare A with D"""
    pass


def inst_cp_a_e(cpu):
    """0xBB: CP A,E - compare A with E"""
    pass


def inst_cp_a_h(cpu):
    """0xBC: CP A,H - compare A with H"""
    pass


def inst_cp_a_l(cpu):
    """0xBD: CP A,L - compare A with L"""
    pass


# Extended instructions (prefix 0xED)
def inst_add_de_a(cpu):
    """0xED 0x36: ADD DE,A - signed add A to DE"""
    # Sign-extend A to 16-bit
    if cpu.A & 0x80:
        val = cpu.A | 0xFF00  # Negative
        val = -(~val & 0xFFFF)
    else:
        val = cpu.A
    cpu.DE = (cpu.DE + val) & 0xFFFF


def inst_nextreg_a(cpu):
    """0xED 0x92 n: NEXTREG n,A - write A to Next register n"""
    reg = cpu.fetch_byte()
    if reg == 87:  # MMU register for slot 7
        # Page switch
        if cpu.A != cpu.mmu7_page:
            # In full emulator: swap pages
            # For Phase 1: only page $20 is allowed
            if cpu.A != 0x20:
                print(f"Warning: MMU7 page ${cpu.A:02X} not yet supported (only $20)")
            cpu.mmu7_page = cpu.A & 0xFF


def inst_nextreg_nn(cpu):
    """0xED 0x91 n m: NEXTREG n,m - write immediate m to Next register n"""
    reg = cpu.fetch_byte()
    val = cpu.fetch_byte()
    if reg == 87:
        if val != 0x20:
            print(f"Warning: MMU7 page ${val:02X} not yet supported (only $20)")
        cpu.mmu7_page = val & 0xFF


def inst_push_nn(cpu):
    """0xED 0x23 nn: PUSH nn - push 16-bit immediate"""
    lo = cpu.fetch_byte()
    hi = cpu.fetch_byte()
    cpu.push(lo | (hi << 8))


def inst_mul_de(cpu):
    """0xED 0x30: MUL D,E - multiply D*E -> DE (unsigned)"""
    result = (cpu.D * cpu.E) & 0xFFFF
    cpu.DE = result


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
        disp = -(~disp & 0xFF)
    addr = (cpu.IX + disp) & 0xFFFF
    cpu.L = cpu.mem[addr]


def inst_ld_h_ixm_disp(cpu):
    """0xDD 0x66 d: LD H,(IX+d) - load H from memory at IX+displacement"""
    disp = cpu.fetch_byte()
    if disp & 0x80:
        disp = -(~disp & 0xFF)
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
    0xC1: inst_pop_bc,
    0xC2: inst_jp_nz_nn,
    0xC3: inst_jp_nn,
    0xC5: inst_push_bc,
    0xC6: inst_add_a_nn,
    0xC9: inst_ret,
    0xCA: inst_jp_z_nn,
    0xCD: inst_call_nn,
    0xD1: inst_pop_de,
    0xD2: inst_jp_nc_nn,
    0xD5: inst_push_de,
    0xD6: inst_sub_a_nn,
    0xD9: inst_exx,
    0xDA: inst_jp_c_nn,
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
    0x23: inst_push_nn,
    0x30: inst_mul_de,
    0x31: inst_ld_hl_de_a,
    0x36: inst_add_de_a,
    0x5B: inst_ld_de_nnm,
    0x73: inst_ld_nnm_sp,
    0x7B: inst_ld_sp_nnm,
    0x91: inst_nextreg_nn,
    0x92: inst_nextreg_a,
}

IX_INSTRUCTION_MAP = {  # 0xDD prefix
    0x21: inst_ld_ix_nn,
    0x66: inst_ld_h_ixm_disp,
    0x6E: inst_ld_l_ixm_disp,
    0xE9: inst_jp_ix,
}
