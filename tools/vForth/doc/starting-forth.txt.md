Starting FORTH
Starting FORTH
An Introductionto the FORTH
Language
       andOperating
                  System
for BeginnersandProfessionals


                 LeoBrodie,
               FORTH. Inc.


                    +
                With a foreword by
                Charles H. Moore




   Prentice-Hall, Inc., Englewood Cliffs, NJ 07632
library of CongressCatalogingin PublicationData
BRODIE, LEO.
    Starting FORTH.

    I. FORTH (Computer program language) I. Title.
QA76.73.F24B76        001.64'24   81-11837
ISBN 0-IJ-842930-8                AACR2
ISBN 0-13-842922-7 (pbk.)




Publisher's credits:
Editorial / production supervision: Kathryn Gollin Marshak
Manufacturing buyer : Gordon Osbourne
Paper cover design: FORTH, Inc. and Alon Jaediker
Case cover design: Edsal Enterprises




 The pages of this book were reproduced
from camera ready copy
 designed and prepared by FORTH, Inc.


© 1981 by FORTH, Inc., Hermosa Beach, CA 90254




All rights reserved. No part of this book
may be reproduced in any form or by any means
without permission in writing from the publisher.




Printed in the United States of America

19 18 17 16 15 14 13 12



Prentice-Hall International, Inc., London
Prentice-Hall of Australia Pty. Limited, Sydney
Prentice-Hall of Canada, Ltd., Toronto
Prentice-Hall of India Private Limited , New Delhi
Prentice-Hall of Japan, Inc., Tokyo
Prentice-Hall of Southeast Asia Pte. Ltd., Singapore
Whitehall Books Limited, Wellington, New Zealand
                               ABOUT THE AUTHOR


Leo Brodie's         inability        to express       even    the most complex
technical     concepts     without adding a twist of humor comes from an
early love of comedy.             He specialized     in playwriting     at UCLA and
has had several        comedies        produced    there    and in local    theater.
He has also written         freelance      magazine articles      and has worked as
a copywriter       for an ad agency.            When a company he was working
for installed       a computer,       he became inspired        to try designing     a
microprocessor-based           toy.    Although he never got the toy running,
he learned     a lot about computers            and programming.       He now works
at FORTH, Inc. as a technical              and marketing      writer,  where he can
play on the computers as the muse determines                  without having to be
a fanatical      computer jockey,          and is allowed      to write books such
as this.

Leo's other interests  include        singing,    driving    classic   Volvos,    and
dancing to 50's music.




                                          V
                                    FOREWORD


The FORTH community can celebrate          a significant       event with the
publication   of Starting     FORTH. A greater         effort,    talent,  and
commitment    have gone into this         book than into any previous
introductory  ~anual.    I, particularly,    am pleased      at this evidence
of the growing popularity     of FORTH, the language.

I developed      FORTH over a period        of some years as an interface
between    me and the computers          I programmed.       The traditional
languages    were not providing      the power, ease, or flexibility         that
I wanted.      I disregarded      much conventional      wisdom in order to
include     exactly     the capabilities        needed     by a productive
programmer . The most important            of these   is the ability     to add
whatever capabilities        later become necessary.
The first time I combined the ideas I had been developing             into a
single entity,    I was working on an IBM 1130, a "third-generation"
computer.     The result    seemed so powerful   that I considered       it a
"fourth -generation      computer  language."   I would have called         it
FOURTH, except       that    the 1130 permitted    only five-character
identifiers    . So FOURTH became        FORTH, a nicer   play on words
anyway.

One principle     that guided the evolution            of FORTH, and continues
to guide its application,         is bluntly:       Keep It Simple.           A simple
solution   has elegance.        It is the result          of exacting      effort     to
understand    the real problem and is recognized                 by its compelling
sense of rightness."      I stress    this point         because     it contradicts
the conventional       view that power i ncreases                with complexity.
Simplicity    provides    confidence,       reliability,         compactness,       and
speed.                                                                      ·

Starting      FORTH was written      and illustrated     by Leo Brodie,      a
remarkably       capable    person whose insight     and imagination    will
become       apparent.       This book is an orig i nal and detailed
prescription       for learning.   It deftly   guides the novice over the
thresholds       of understanding     that all FORTH programmers        must
c r oss.

Although I am the only p e rson who has never had to learn FORTH,
I oo know that its study is a formidabl e one.       As with a human
language,     the usage    of many words must be memorized.          For
beginners,     Leo's droll   comments and supe r bly cast characters
appear     to make this study easy and enjoyable.      For those like
myself     who al r eady know FORTH, a quick reading      provides       a


                                          vi i
delightful  trip and fresh views of familiar    terrain.   But I hope
this book is not so easy and enjoyable     that it seems trivial.   Be
warned that there is heavy content     here and that you can learn
much about computers and compilers  as well as about programming.

FORTH provides      a natural     means of communication          between man and
the smart machines         he is surrounding     himself with.        This requires
that   it share    characteristics         of human languages,            including
compactness,     versatility,      and extensibility.        :t: cannot imagine a
better   language     for writing     programs,     expressing      algorithms,     or
understanding     computers.       As you read this book, I hope that you
may come to agree.


Charles    H. Moore
Inventor    of FORTH




                                        viii
                              ABOUT THIS BOOK


Welcome to Starting   FORTH, your introduction             to an exciting      and
powerful computer language  called  FORTH.

If you're     a beginner    who wants to learn  more about computers,
FORTH is a great         way to learn.   FORTH is more fun to write
programs      with than     any language   that I know of.   (See the
"Introduction     for Beginners.")
If you are a seasoned     professional   who wants to learn FORTH, this
book is just what you need.         FORTH is a very different     approach
to computers,   so different     that everyone,   from newcomers to old
hands, learns   FORTH best from the ground up. If you're adept at
other computer languages,      put them out of your mind, and remember
only what you know about computers.          (See the "Introduction      for
Professionals, '1)

Since many people      with different     backgrounds     are interested    in
FORTH, I've arranged      this book so that you'll       only have to read
what you need to know, with footnotes             addressed    to different
kinds of readers.    The first half of Chap. 7 provides         a background
in computer arithmetic      for beginners   only.
This book explains       how to write simple applications         in FORTH. It
includes    all standard       FORTH words that          you need to write    a
high-level,      single-task      application.           This word set is an
extremely    powerful     one, including       everything     from simple math
operators     to compiler-controlling             words.     (See Appendix   3,
"FORTH-79 Standard.")

Excluded from this book are all commands that are r e lated to the
assembler,    multiprogrammer,  printing  and disking    utilities,       and
target   compiler.    These commands are available    on some versions
of FORTH such as polyFORTH.       (See Appendix 2, "Further         Features
of polyFORTH. ")

I've chosen   examples  that will actually       work at a FORTH system
with a terminal    and disk.    Don't infer    from this that FORTH is
limited  to batch or string - handling    tasks, since there   is really
no limit to FORTH's use fulne s s.

Here are some features       of this   book that   will   make it easy   to use:

All commands    are listed    twice:    first,   in the   section   in which   the



                                        ix
word is introduced,        and second, in the summary at the end of that
chapter.   Appendix       4 provides  an index to the tables.

Each chapter    also has a review of terms         and   a set   of exercise
problems.   Appendix 1 lists the answers.

Several  "Handy Hints" have been included    to reveal   procedural
tips or optional   routines that are useful for learners    but that
don't merit an explanation  as to how or why they work.

A personal     note:      FORTH is a very unusual language.        It violates
many cardinal      rules of programming.        My first reaction     to FORTH
was extremely       skeptical,    but as I tried   to develop     complicated
applications     I began to see its beauty and power.           You owe it to
yourslf     to keep an open mind while reading           about some of its
peculiarities.        I'll   warn you now:     few programmers      who learn
FORTH ever go back to other languages.

Good luck,    and enjoy    learning!


Leo Brodie
FORTH, Inc.




                                       X
                              ACKNOWLEDGEMENTS


I'd like to thank      the   following    people    who helped     to make this
book possible:

For consultation         on FORTH technique       and style:      Dean Sanderson,
Mich ae l LaManna, Jam e s Dewey, Edward K. Conklin,                and Elizabeth
D. Rather, all of FORTH, Inc.; for providing               insights   into the art
of teaching       FORTH and for writing      several     of the problems in this
book:     Kim Harris of the FORTH Interest            Group; for proofreading,
editorial      suggestions,      and enormous amounts of work formatting
the pages:       Carolyn A. Rosenberg;       for help with typing         and other
necessities:         Sue Linstrot,   Carolyn     Lubisich,    Kevin Weaver, Kris
Cramer, and Stephanie           Brown Brod i e; for help with the graphics:
Carolyn      Lubisich,      Jim Roberts,    Janine     Ritscher,     Dana Rather,
Winnie Shows, Natasha Elbert,           Barbara Roberts, and John Dotson of
Sunrise     Printery     (Redondo Beach, CA); for technical            assistance,
Bill Patterson        and Gary Friedlander;        for constructive      criticism,
much patience           and love:      Stephanie       Brown Brodie;        and for
inventing      FORTH, Charles H. Moore.




                                         xi
                        TABLE OF CONTENTS


ABOUT THE AUTHOR                                                            V

FOREWORDby Charles       H. Moore                                         vii
ABOUT THIS BOOK                                                            ix

ACKNOWLEDGEMENTS                                                           xi
INTRODUCTIONS                                                                   1
    Introduction      for Beginners                                             1
    Introduction    . for Professionals                                         3

1   FUNDAMENTALFORTH                                                            7
     A Living Language                                                          7
     All This and ••• Interactive!                                              9
     The Dictionary                                                         14
     Say What?                                                              18
     The Stack:    FORTH's Worksite        for Arithmetic                   19
     Postfix  Power                                                         22
     Keep Track of Your Stack                                               24
     Review of Terms                                                        27
     Problems                                                               29

2   HOW TO GET RESULTS                                                      31
     FORTH Arithmetic - -Calculator       Style                             31
     For Adventuresome       Newcomers Sitting     at a Terminal            33
     Postfix    Practice   Problems (Quizzie 2-a)                           37
     FORTH Arithmetic       - Definition    Style                           38
     Definition-style      Practice   Problems (Quizzie 2-b)                41
     The Division      Operators                                            42
     Stack Maneuvers                                                        44
     Stack Manipulation        and Math Definitions    (Qui zz i e 2-c)     51
     Playing    Doubles                                                     52
     Review of Terms                                                        54
     Problems                                                               55

3   THE EDITOR (AND STAFF)                                                  57
     Another Look at the Dictionary                                         57
     How FORTH Uses the Disk                                                59
     Dear EDITOR                                                            63
     Character    Editing Commands                                          66
     The Find Buffer and the Insert Buffer                                  69
     Line Editing Commands                                                  73
     Miscellaneous     EDITOR Commands                                      75
     Getting !LOAD!ed                                                       79
     Review of Terms                                                        86
     Problems                                                               87

                                    xiii
4   DECISIONS,      DECISIONS,    •••                         89
    The Conditional  Phrase                                   89
    The Alternative Phrase                                    92
    Nested ~ ••• THEN Statements                              93
    A Closer Look at IF                                       95
    A Little Logic                                            97
    Two Words with Built-in  [!!:ls                          101
    Review of Terms                                          104
    Problems                                                 105

5   THE PHILOSOPHY OF FIXED POINT                            107
     Quickie Operators                                       107
     Miscellaneous     Math Operators                        108
     The Return Stack                                        109
     An Introduction     to Floating-Point      Arithmetic   113
     Why FORTH Programmers Advocate           Fixed-Point    114
     Star-slash    the Scalar                                116
     Some Perspective      on Scaling                        119
     Using Rational     Approximations                       121
     Review of Terms                                         124
     Problems                                                125

6   THROWIT FOR A LOOP                                       127
     Definite   Loops -- ~ ••. ILOOPI                        127
     Getting [g}fy                                           131
     Nested Loops                                            132
      +LOOP                                                  133
      DOing It -- FORTH Style                                135
     Indefinite   Loops                                      138
     The Indefinitely    Definite Loop                       140
     Review of Terms                                         144
     Problems                                                145

7   A NUMBEROF KINDS OF NUMBERS                              149
    I. FOR BEGINNERS                                         150
     Signed   vs.   Unsigned     Numbers                     150
     Arithmetic     Shift                                    153
     An Introduction      to Double-length    Numbers        154
     Other Number Bases                                      155
     The ASCII Character        Set                          156
     Bit Logic                                               158
    II. FOR EVERYBODY                                        160
      Signed and Unsigned Numbers                            160
     Number Bases                                            162
      Double - length Numbers                                164
     Number Formatting       -- Double-length   Unsigned     166
     Number Formatting       -- Signed and Single-length     170
      Double-length     Operators                            173
      Mixed-length     Operators                             174
     Numbers in Definitions                                  176
      Review of Terms                                        180
      Problems                                               181



                                        xiv
8 VARIABLES,CONSTANTS,ANDARRAYS                    183
   Variables                                       183
   A Closer Look at Variables                      186
   Using a Variable as a Counter                   188
   Constants                                       190
   Double-length Variables and Constants           193
  Arrays                                           195
  Another Example -- Using an Array for Counting   199
  Factoring Definitions                            202
  Another Example -- "Looping" through an Array    204
  Byte Arrays                                      206
  Initializing  an Array                           207
  Review of Terms                                  211
  Problems                                         212
9 UNDERTHE HOOD                                    215
   Inside !INTERPRET!                              215
   Vectored Execution                              217
   The Structure of a Dictionary Entry             220
   The Basic Structure of a Colon Definition       224
   Nested Levels of Execution -                    225
   One Step Beyond                                 228
   Abandoning the Nest                             229
   FORTHGeography                                  231
   The Geography of a Multi - tasked FORTHSystem   238
   User Variables                                  240
   Vocabularies                                    242
   Review of Terms                                 248
   Problems                                        251

10 I/0 ANDYOU                                      253
   Block Buffer Basics                             253
   Output Operators                                258
   Outputting Strings from Disk                    261
   Internal String Operators                       266
   Single - character Input                        268
   String Input Commands, from the Bottom up       270
   Number Input Conversions                        277
   A Closer Look at IWORDI                         280
   String Comparisons                              281
   Review of Terms                                 286
   Problems                                        287




                             xv
11 EXTENDINGTHE COMPILER:
   DEFINING WORDSANDCOMPILINGWORDS               289
    Just a Question of Time                      289
    How to Define a Defining Word                290
    Defining Words You Can Define Yourself       293
    How to Control the Colon Compiler            299
    More Compiler-controlling  Words             303
    An Introduction  to FORTH Flowcharts         307
    Curtain Calls                                309
    Review of Terms                              314
    Problems                                     315
12 THREE EXAMPLES                                317
    IWORDIGame                                   318
    File Away!                                   328
    No Weighting                                 341
    Review of Terms                              348

APPENDICES
     1.   Answers to Problems
     2.   Further   Features   of polyFORTH
     3.   FORTH-79 Standard
     4.   Summary of FORTHWords



                          TABLE OF HANDYHINTS
A Non-Destructive  Stack Print                    50
When a Block Won't IL?ADI                         82
A Better Non-Destructive  Stack Print            83
How to Clear the Stack                           137
!PAGE)and !QUIT)                                 142
A Definition  for BINARY-- or Any-ARY            163
How to ILOCATEIa Source Definition               245
A Random Number Generator                        265
Two Convenient Additions to the Editor           269
Entering Long Definitions   from Your Terminal   306




                                   xvi
Starting FORTH
                              INTRODUCTIONS

Introduction    for Beginners:     What Is a Computer Language?

At first,   when beg inners      hear
the term "computer       language,"
they wonder,        "What kind of
language       could   a computer
possibly     speak?     It must be
 awfully    hard for people         to
understand.      It probably    looks
like:
           976# !@NX714&+

if it   looks   like   anything     at
all."
Actually,     a computer language
should      not be difficult      to
understand.        Its purpose    is
simply to serve as a convenient
compromise      for communication
between person and computer.
Consider     the marionette.        You
can make a marionette           "walk"
simply by working the wooden
control,    without even touching
the strings.     You could say that
rocking      the control        means
"wal king" in the language of the
marionette.         The puppeteer
guides the marionette         in a way
 that    the    marionette         can
understand         and     that   the
puppeteer can easily master.
Computers are machines just like
the marionette.      They must be
told exactly      what to do, in
specific   language.     And so we
need a language which possesses
two seeming l y opposite traits:


                                      1
2                                                              Starting      FORTH




On the one hand, it must be precise           in its meaning   to the
computer, conveying    all the information    that the computer needs
to know to perform the operation.       On the other hand, it must be
simple and easy-to-use    by the programmer.
Many languages have been developed since the birth of computers:
FORTRAN is the elder        statesman     of the field;   COBOL is the
standard   language     for business     data processing;    BASIC was
designed    as a beginner's       language     along  the road toward
languages   like FORTRAN and COBOL. This book is about a very
different kind of language:       FORTH. FORTH's popularity    has been
gaining steadily    over the past several years, and its popularity
is shared among programmers in all fields.
All the languages      mentioned above, including       FORTH, are called
"high-level"       languages.       It's important     for beginners     to
recognize    the difference     between a high-level     language and the
computer it runs on. A high-level         language looks the same to a
programmer regardless         of which make or model of computer it's
running     on.   But each make or model has its own internal
language,     or "machine language."        To explain     what a machine
language is, let's return to the marionette.
Imagine that there is no wooden control          and that the puppeteer
has to deal directly    with the strings.   Each string corresponds     to
exactly    one part of the marionette's         body.    The harmonious
combinations   of movements of the individual          strings  could be
called the marionette's     "machine language."
Now tie the strings     to a control.    The
control   is like a high-level    language.                            a high-level
With a simple      turn of the wrist,    the                          symbol used in
puppeteer       can move many strings                                  your program
simultaneously.
So it is with a high-level
language,
symbol"+"
functions
                                computer
            where the simple and familiar
                causes    many internal
           to be performed in the process
                                                             •
                                                        high-level
                                                        language
of addition .
Here's
computer:
translate
           a very clever          thing
                 it can be programmed
              high-level
                                           about
                               symbols (such as
                                                   a
                                                  to         •
                                                          machine
                                                        instruction
 "+") into the computer's             own machine         machine
language.      Then it can proceed to carry             instruction       machine
out the      machine        instructions.           A                     language
high-level        language        is a computer           machine
                                                        instruction
program       that     translates         humanly
understandable        words and symbols into              machine
the machine language           of the particular        instruction
make and model of computer.
Starting   FORTH                                                           3




 What's the difference    between   FORTH and other high-level
languages?    To put it very briefly:     it has to do with the
compromise between man and computer.        A language   should be
designed for the convenience   of its human users, but at the same
time for compatibility with the operation of the computer.
FORTH is unique among languages    because its          solution   to this
problem is unique. This book will explain how.




Introduction   for Professionals:     FORTH in the Real World

FORTH has enjoyed a rising tide of popularity             in recent years,
perhaps most visibly       among enthusiasts      and hobbyists.    But this
development     is only a new wrinkle in the history             of FORTH.
FORTH has been in use for over ten years in critical             scientific
and industrial      applications.        In fact,   if you use a mini- or
microcomputer     professionally,       chances are that FORTH can run
your application--more         efficiently     than the language      you're
presently using.
Now you'll probably ask rhetorically,   "If FORTH is so efficient,
how come I'm not using it?"     The answer is that you, like most
people, don't know what FORTHis.
To really get an understanding   of FORTH, you should read this
book and, if possible,     find a FORTH system and try it for
yourself.   For those of you who are still     at the bookstore
browsing, however, this section will answer two questions:  "What
is FORTH?" and "What is it good for?"
FORTHis many things:
     --a high-level  language
     --an assembly language
     --an operating system
     --a set of development tools
     --a software design philosophy
As a language,      FORTH begins with a powerful set of standard
commands, then provides the mechanism by which you can define
your own commands.            The structured     process   of building
definitions    upon previous definitions      is FORTH's equivalent    of
high-level    coding.    Alternatively,  words may be defined directly
in assembler mnemonics, using FORTH's assembler.           All commands
are interpreted     by the same interpreter    and compiled by the same
compiler, giving the language tremendous flexibility.
The highest    level   of your code will resemble    an English-language
4                                                                       Starting   FORTH




description       of your application.              FORTH has             been called   a
"meta-application       language"--a           language  that             you can use to
create problem-oriented      languages.
As  an operating     system, FORTH does everything     that traditional
operating     systems do, including    interpretation,      compilation,
assembling, virtual memory handling,     I/O, text editing,    etc.
But because the FORTH operating     system is much simpler than its
traditional counterparts   due to FORTH's design, it runs much more
quickly, much more conveniently,   and in far less memory.
What is FORTH good for?            FORTH offers a simple means to maximize
a processor's efficiency.           For example:
FORTH is fast.       High-level      FORTH executes     faster   than other
high-level     languages        and between       20 and 75% slower     than
equivalent   assembly-language         programs, while time-critical     code
may be written       in assembler       to run at full processor      speed.
Without    a traditional        operating      system,  FORTH eliminates
redundancy and needless run-time error checking.
FORTH compiled code is compact.       FORTH applications    require less
memory than their      equivalent     assembly-language       programs!
Written in FORTH, the entire      operating   system and its standard
word set reside    in less than BK bytes.         Support for a target
application  may require less than lK bytes.
FORTH is transportable.                It has been      implemented         on just   about
every    mini-   and   microcomputer       known   to   the   industry.

FORTH has been known to cut program development          time by a factor
of ten for equivalent      assembly-language      programming      and by a
factor      of two for equivalent         high-level       programming.
Productivity     increases    because   FORTH epitomizes       "structured
programming" and because it is interactive         and modular.
Here are a few samples          of FORTH in the real           world:
        Process    Control--FORTH      is being used to steer           the robot
        motion-picture     cameras to create the special        effects    used in
        the film "Battle        Beyond the Stars."        FORTH was chosen
        because    of its speed and its flexibility           in providing      an
        interface     by which the operator      can describe        the camera
        motion.     Other process-control      applications       range from a
        baggage handler       for a major U.S. airline      to a peach sorter
        for a California     cannery.
        Portable     Intelligent    Devices--The      variety    of applications
        which run FORTH internally             include     a heart   monitor     for
        outpatients,       an automotive    ignition    analyzer,    a hand-held
        instrument to measure relative         moisture in different      types of
        grain, and the Craig Language Translator.
Starting FORTH                                                                     5




     Medical--On a single PDP-11 at a major hospital,      FORTH
     simultaneously maintains a large patient database; manages
     thirty-two    terminals and an optical   reader;  performs
     statistical   analysis    on the database    to correlate  physical
     types, diseases,    treatments,  and results;   and analyzes blood
     samples and monitors heartbeats      in real time.
     Data Acquisition        and Analysis--A       single   PDP-11/34 running
     under FORTH controls          an entire     observatory,       including     an
     extraordinarily       accurate   telescope,      the dome, several CRTs,
     a clock, a line printer,         and a floppy disk drive--and            still
     has time for taking data on infrared               emissions from space,
     analyzing the data, and displaying            the results on a graphics
     monitor.      Applications     of this type often make use of Fast
     Fourier and Walsh Transforms,            numerical       integration,      and
     other math routines written in FORTH.
There's     a catch,   we must admit.     It is that FORTH makes .YQ!!
responsible     for your computer's efficiency.     To draw an analogy:
a manual transmission     is tougher to master than an automatic, yet
for many drivers it offers improved control over the vehicle.
Similarly, FORTH is tougher to master than traditional       high-level
languages,  which essentially   resemble one another       (i.e., after
learning   one, it is not difficult     to learn   another).        Once
mastered,  however, FORTH gives you the capability        to minimize
CPU time and memory space, as well as an organizing         philosophy
by which you can dramatically  reduce project development time .
And remember, all of FORTH's elements enjoy the same protocol,
including   operating  system, compiler,   interpreters,  text editor,
virtual   memory, assembler,   and multiprogrammer.      The learning
curve for FORTH is much shorter than that for all these separate
elements added together.

If any of this     sounds   exciting     to you, turn     the page     and start
FORTH.
                             1     FUNDAMENTAL FORTH


In this chapter     we'll   acquaint     you with some of the unique
properties of the FORTH language.        After a few introductory pages
we'll have you sitting    at a FORTH terminal.      If you don't have a
FORTH terminal,  don't worry.        We'11 show you the result of each
step along the way.


A Living   Language

Imagine that you're an office     manager and you've just hired a
new, eager assistant.   On the first day, you teach the assistant
the proper   format for typing   correspondence.    (The assistant
already  knows how to type.)   By the end of the day, all you have
to say is "Please type this."
On the second day, you explain     the filing                system.  It takes all
morning to explain  where everything     goes,               but by the afternoon
all you have to say is "Please file this."
By the end of the week, you can communicate              in a kind of
shorthand,  where "Please send this letter"     mean-s "Type it, get me
to sign it, photocopy    it, file the copy, and mail the original."
Both you and your assistant       are free to carry out your business
more pleasantly  and efficiently.

Good organization     and effective          communication     require      that   you
     1.    define   useful       tasks   and give   each task a name, then
     2.    group related         tasks together into      larger    tasks     and give
           each of these         a name, and so on.
FORTH lets you organize            your own procedures   and communicate them
to a computer   in just           this way (except     you don't have to say
"Please").

As an example,    imagine   a microprocessor-controlled         washing
machine   programmed    in FORTH. The ultimate          command in your
example is named WASHER. Here is the definition            of WASHER, as
written in FORTH:



                                            7
8                                                            Starting   FORTH




     : WASHER       WASH SPIN RINSE SPIN ;

In FORTH, the colon indicates        the beginning  of a new definition.
The first  word after     the colon,    WASHER, is the name of the new
procedure.     The remaining     words, WASH, SPIN, RINSE, and SPIN,
comprise   the "definition"      of the new procedure.      Finally,     the
semicolon   indicates   the end of the definition.




          0                                                         0
          0                                                         SJ

Each of the       words compr1s1ng        the definition      of WASHER has
already  been     defined   in our washing-machine         application. For
example, let's     look at our definition     of RINSE:
     : RINSE      FILL AGITATE DRAIN;

As you can see, the definition             of RINSE consists  of a group of
words:      FILL, AGITATE, and DRAIN. Once again,            each of these
words has been already         defined    elsewhere in our washing-machine
application.      The definition      of FILL might be

     : FILL      FAUCETS OPEN TILL-FULL         FAUCETS CLOSE ;

In this definition    we are referring    to things (faucets)  as well as
to actions      (open and close).       The word TILL-FULL      has been
defined    to create   a "delay    loop" which does nothing      but mark
time until the water-level      switch has been activated,    indicating
that the tub is full.

If we were to trace    these definitions        back, we would eventually
find that they are all defined         in terms of a group of very useful
commands that form the basis of all FORTH systems.             For example,
polyFORTH     includes   about    300 such commands.         Many of these
commands are themselves     "colon definitions"       just like our example
words; others are defined     directly     in the machine language    of the
particular   computer . In FORTH, a defined           command is called     a
"word." t




t For Old Hands
This meaning   of "word" is not to          be associated     with a 16-bit
value, which in the FORTH community         is referred   to as a "cell."
1 FUNDAMENTAL
          FORTH                                                               9




The ability      to define a word in terms of other words is called
"extensibility."       Extensibility      leads to a style of programming
that is extremely         simple,    naturally    well-organized,   and as
powerful as you want it to be.
Whether your application    runs an assembly line, acquires data for
a scientific  environment,     maintains a business  application, or
plays a game, you can create your own "living language" of words
that relate to your particular    need.
In this book we' 11 cover       the most useful   of the standard          FORTH
commands.


All This and ... Interactive!

One of FORTH's many unique        features  is that  it lets you
"execute   t a word by simply naming the word. If you're working
          11


at a terminal   keyboard, this can be as simple as typing in the
word and pressing the RETURNkey.
Of course, you can also use the same word in the definition                   of
any other word, simply by putting its name in the definition.
FORTH is called an "interactive"   language        because    it carries     out
your commands the instant you enter them.
We're going to give an example that you can try yourself, showing
the process   of combining    simple commands into more powerful
commands.   We'11 use some simple FORTH words that control      your
terminal screen or printer.     But first, let's get acquainted with
the mechanics    of "talking"    to FORTH through your terminal's
keyboard.

                      Take a seat at your real or
                      imaginary    FORTH terminal.
                      We'11 assume that someone
                      has been kind enough to
                      set everything    up for you,
                      or that you have followed
                      all the instructions    given
                      for loading your particular
                      computer.


t For Beginners
To "execute"      a word is to order      the   computer     to carry      out a
command.
10                                                                   Starting     FORTH




Now press      the key labeled:

       RETURNt

The computer          will   respond   by saying

       ok
The RETURN key is your way of telling       FORTH to acknowledge       your
request.     The ok is FORTH's way of saying            that     it's done
everything   you asked it to do without any hangups.         In this case,
you didn't  ask it to do anything,    so FORTH obediently      did nothing
and said ok.     (The ok may be either     in upper case or in lower
case, depending    on your terminal.)

Now enter         this:

       15 SPACES

If you make a typing      mistake, you can correct   it by hitting   the
 "backspace"      key.   Back up to the mistake,   enter  the correct
letter,   then continue.     When you have typed the line correctly,
press the RETURN key.        (Once you press RETURN, it's too late to
correct    the line.)
In this book, we use the symbol mm, to mark the point where you
must press   the RETURN key.   We also underline   the computer's
output  (even though the computer   does not) to indicate  who is
typing what.

Here's      what has happened:
         15 SPACESC!ii!lmJ
                         ________                    o_k

As soon as you pressed       the return    key, FORTH printed      fifteen
blank    spaces    and then,    having   processed      your request,      it
responded    ok (at the end of the fifteen     spaces).
Now enter         this:

         42 EMITmi!lmJ *ok
The phrase            "42 EMIT" tells       FORTH to print    an asterisk         (we'll



tFor     People      at Terminals

RETURN may have a different       name on your                  terminal.         Other
possib l e names are NEW LINE and ENTER.

Backspace may also             have    a different    name on your    terminal,     such
as DEL or RUBOUT.
1 FUNDAMENTALFORTH                                                                          11




discuss this      command later on in the book.)                      Here FORTH printed
the asterisk,     then responded ok.

We can put more than one command on the same line.                             For example:
        15 SPACES 42 EMIT 42 EMITtm!lm)                                          **ok
This time FORTH printed fifteen spaces and two asterisks.      A note
about entering    words and/or numbers: we can separate    them from
one another by as many spaces as we want for clarity.        But they
must be separated    by .il_ least one space for FORTH to be able to
recognize them as words and/or numbers.
Instead     of entering        the phrase
        42 EMIT
over and over,         let's     define    it as a word called         "STAR."
Enter this
        : STAR       42 EMIT ;tm!Jlm ok
Here "STAR" is the name; "42 EMIT" is the definition.         Notice
that we set off the colon and semicolon from adjacent words with
a space.   Also, to make FORTH definitions     easy for human beings
to read, we conventionally    separate     the name of a definition
from its contents with three spaces.
After     you have     entered       the   above    definition       and   pressed      RETURN,
FORTH responds    ok, signifying                    that it has         recognized        your
definition and will remember it.                   Now enter
        STARtm!Jlm     *ok
Voila!    FORTH executes             your definition             of "STAR" and prints        an
asterisk.
There is no difference   between a word such as STAR that you
define yourself and a word such as !EMIT! that is already defined.
In this book, however, we will put boxes around those words that
are already    defined, so that you can more easily       tell  the
difference.
Another system-defined   word is [ID, which performs a carriage
return and line feed at your terminal.t For example, enter this:


tFor Beginners
Be sure to distinguish               between       the key labeled         RETURN and the
FORTHword 1£Bl.
12                                                                               Starting        FORTH




        CRmi!llm
        ok      -

As you can see,           FORTH executed       a carriage           return,      then     printed      an
ok (on the next           line).

Now try       this:

        CR STAR CR STAR CR STARmi!lmJ
        *
        T
        *ok

Let's       put a (g]J in a definition,           like   this:

        : MARGIN          CR 30 SPACES ;mi!lmJok

Now we can enter

            MARGIN STAR MARGIN STAR MARGIN STARmi!lmJ

and get        three    stars   lined   up vertically,           thirty       spaces     in from the
left.

Our MARGIN STAR combination                 will     be useful        for what we intend               to
do, so let's define

        : BLIP         MARGIN STAR ;mi!lmJok

We will also need               to print     a horizontal   row of stars.  So let's
enter  the following              definition     (we'll explain   how it works in a
later chapter):

        : STARS          O DO STAR LOOP ;mi!lmJok

Now we can say

        5 STARSmi!lmJ *****ok

or

        35 STARSmi!llm ***********************************ok

or any number of stars              imaginable!

We will need a word which performs                           MARGIN, then               prints      five
stars. Let's define it like this:

        : BAR          MARGIN 5 STARS ;ml!llm ok

Now we can enter
        BAR BLIP BAR BLIP BLIP              CR
1 FUNDAMENTAL
            FORTH                                                            13




and get a letter      "F" (for FORTH) made up of stars.       It should look
like this:

                                 *****
                                 *
                                 *****
                                 *
                                 *
The final step      is to make this   new procedure    a word.    Let's    call
the word "F":
     : F       BAR BLIP BAR BLIP BLIP CR ;CIJl!llmok
You've just seen an example of the way simple FORTHcommands can
become the foundation        for more complex commands.       A FORTH
application,   when listed,t    consists of a series of increasingly
powerful definitions   rather than a sequence of instructions     to be
executed in order.
To give you a sample of what a FORTH application        really            looks
like, here's a listing of our experimental application:

      0    (   LARGE LETTER-F>
      1        STAR   42 EMIT ;
      2        STARS   0 DO STAR LOOP ;
      3        MARGIN   CR 30 SPACES;
      4        BLIP   MARGIN STAR;
      5        BAR   MARGIN 5 STARS;
      6        F   BAR BLIP BAR BLIP BLIP       CR
      7
      8




tFor Beginners
We'll explain       more about   listing,   as it   applies   to FORTH, in
Chapter 3.
14                                                        Starting   FORTH




The Dictionary

Each word and its definition       are
entered into FORTH's "dictionary."
The dictionary    already contained
many words when you started,       but
your own words are now in the
dictionary   as well.
When you define a new word, FORTH
translates      your definition  into
dictionary       form and writes  the
entry      in the dictionary.    This
process is called "compiling. "t



        : STAR        't2 EMIT ;         For example,    when you enter
                                         the line
                                              : STAR    42 EMIT ;Cll!Iim
                                         the compiler compiles the new
                                         definition    into the dictionary.
                                         The compiler       does not print
                                         the asterisk.           --



Once a word is in the dictionary,     how is it executed?         Let's say
you enter the following line directly    at your terminal       (not inside
a definition):
       STAR 30 SPACES~
This will activate       a word called   !INTERPRET!, also   known as the
"text interpreter."




tFor   Beginners
Compilation  is a general computer term which normally means the
translation  of a high-level    program into machine code that the
computer can understand.      In FORTH it means the same thing, but
specifically  it means writing in the dictionary.
1 FUNDAMENTAL FORTH                                               15




The text interpreter  scans        When he finds such a string,
the input stream, looking for      he looks it up in the
strings of characters  separated   dictionary.
by spaces.




If he finds the word in the        --who then executes the
dictionary,    he points out       definition  (in this case,
the definition    to a word        he prints an asterisk).    The
called !EXECUTE!   --              interpreter  says everything's
                                   "ok."




If the interpreter      cannot     !NUMBER! knows a number when
find the string in the             he sees one. If [NUMBER!
dictionary,   he calls the         finds a number, he runs it
numbers-runner     (called         off to a temporary storage
!NUM
   BER!).                          location  for numbers.
16                                                          Starting     FORTH




What happens when you try to execute a word that             is not in the
dictionary?  Enter this and see what happens:
     XLERBC!lil!Im)
                 XLERB?




                                                                           ?•



When the text interpreter    cannot find XLERB in the dictionary, it
tries to pass it off on !NUMBER!. INUMBERI shines it on. Then the
interpreter  returns the string to you with a question mark.
In some versions      of FORTH, including   polyFORTH, the compiler
does not copy the entire          name of the definition   into the
dictionary--only      the first three characters   and the number of
characters.      For example,   in polyFORTH, the text interpreter
cannot distinguish     between STAR and STAG because both words are
four characters    in length and both begin S-T-A.t
While many professional   programmers prefer the three-character
rule because    it saves memory, certain     programmers   and many
hobbyists  enjoy the freedom to choose ~ name. The FORTH-79
Standard   allows up to thirty-one   characters     of a name to be
stored in the dictionary.
To summarize:     when you type a pre-defined        word at the terminal,
it gets interpreted    and then executed.
Now remember we said      that~       is a word?   When you type       the word
[;], as in
         STAR   42 EMIT ; mI!IiID

t For polyFORTH Users
The trick   to avoiding   conflicts     is to
     a) be conscious of your name choices, and
     ~  when naming     a series   of similar     words,           put     the
        distinguishing character up front, like this:
            lLINE   2LINE 3LINE etc.
1 FUNDAMENTAL
           FORTH                                       17



the following   occurs:



          ~

-.--~ ~--R ---,fJ4~2---tE"['9a-lMI
                   ......
                    T

The text interpreter  finds          and oints it out to
the colon in the input               EXECUTE.
stream,



                                     STAR      42 EMIT




!EXECUTEjsays, "Please        The compiler translates     the
start compiling."             definition  into dictionary
                              form and writes       it in the
                              dictionary.




When the compiler gets        and execution returns to the
to the semicolon, he          text interpreter, who gives
stops,                        the message ok.
18                                                                Starting       FORTH




Say What?


In FORTH, a word is a character    or group of characters that have
a definition.   Almost any characters      can be used in naming a
word. The only characters    that cannot be used are:


     return                  because       the    computer        thinks         you've
                             finished    entering,t

     backspace               because    the computer   thinks        you're       trying
                             to correct    a typing error,

     space                   because the computer        thinks    it's    the    end of
                             the word, and

     caret     rt or A)      because      the editor    (if you 're using   it)
                             thinks     you mean something       else.    We'll
                             discuss    the editor   in Chap. 3.


Here is a FORTH word whose name consists            of two punctuation
marks.    The word is ~ and is pronounced      dot-quote.     You can use
G::] inside   a definitiont     to type a "string"      of text   at your
terminal.    Here's an example:

             GREET   . " HELLO, I SPEAK FORTH " ;mmlm ok

We've just defined   a word called   GREET. Its definition  consists
of just one FORTH word, G::], followed   by the text we want typed.
The quotation   mark at the end of the text will not be typed;       it
marks the end of the text.   It's called  a "delimiter."




tFor    Philosophers

No, the computer    doesn't   "think."       Unfortunately,    there's   no
better   word for what it really       does.     We say "think"      on the
grounds that it's all right    to say, "the lamp needs a new light
bulb."   Whether the lamp really     needs a bulb depends       on whether
it needs to provide    light (that is, incandescence        is its karma).
So let's just say the computer thinks.

tFORTH-79 Standard
In systems       that conform to the     Standard,    ~ will       execute       outside
of a colon       definition  as well.
1 FUNDAMENTAL
            FORTH                                                                 19




When entering          the definition    of GREET, don't        forget   the closing
Ii] to end the definition.
Let's execute       GREET:
        GREETmI!ill3    HELLO, I SPEAK FORTH ok


The Stack:       FORTH's Worksite for Arithmetic

A computer would not be much good if it couldn't do arithmetic.
If you've never studied     computers before,  it may seem pretty
amazing that a computer (or even a pocket calculator)       can do
arithmetic  at all.  We can't cite all the mechanics in this book,
but believe us, it's not a miracle.
In general,     computers  perform their     operations by breaking
everything   they do into ridiculously    tiny pieces of information
and ridiculously    easy things to do. To you and me, "3 + 4" is
just "7," without     even thinking.     To a computer,   "3 + 4" is
actually a very long list of things to do and remember.
Without getting   too specific,    let's say you have a pocket
calculator which expects its buttons to be pushed in this order:




in order to perform the addition and display                  the result.    Here's a
generalized picture of what might occur:



                                                     Name of Next
                                                       Operation




--the    number 3 goes into one place           (called   Box A).
                                                     Name of Next
                                                       Operation


                                                          +
--the    intended      opera t ion (addition)   is remembered somehow.
20                                                                Starting    FORTH




                                                 Name of Next
                                                   Operation


                                                     +
--the    number 4 is stored   into   a second   place    (called     Box B).

                                                 Name of Next
                                                   Operation




--the calculator       performs  the operation    that           is stored in the
"Next Operation"        Box on the contents    of the           number boxes and
leaves the result     in Box A.

Many calculators    and computers approach arithmetic      problems in a
way similar    to what we've just described.       You may not be aware
of it, but these machines are actually      storing   numbers in various
locations   and then performing operations     on them.

In FORTH, there       is one central   location   where numbers                  are
temporarily    stored before being operated     on. That location                  is
called   the "stack."     Numbers are "pushed onto the stack,"                   and
then operations     work on the numbers on the stack.
The best way to explain         the stack is to illustrate              it.    If you
enter the following line      at your terminal:


here's   what happens,   key by key.




Recall that when you enter a number at your terminal,     the text
interpreter     hands it over to INUMBERI, who runs it to some
location.     That location, it can now be told, is the stack.   In
short,    when you enter the number three from the terminal,    you
push it onto the stack.
1 FUNDAMENTAL FORTH                                                    21




Now the four goes   onto   the   "top"   of the   stack   and pushes   the
three downward.




                                                                       ,,



The next word in the input stream can be found in the dictionary.
l±Jhas been previously defined to~ake the top two numbers off
the stack, add them, and push the result back onto the stack."
22                                                                   Starting       FORTH




The next word, G], is also found in the dictionary.                          It has been
previously   defined to take the number off the stack                       and print  it
at the terminal.



Postfix       Power


Now wait,          you say.   Why does       FORTH want you to type

        3 4 +

instead       of

        3   + 4
which       is more familiar       to most people?

FORTH uses "postfix"   notation     (so called     because   the operator    is
affixed   after the numbers)      rather    than     "infix"    notation   (so
called  because the operator    is affixed     in-between     the numbers) so
that all words which "need" numbers can get them from the stack. t




tFor      Pocket-calculator        Experts

Hewlett-Packard           calculators    feature    a stack   and postfix       arithmetic.
1 FUNDAMENTAL
           FORTH                                                                       23




For example:

     the word l±] gets        two numbers from the stack        and adds them;

     the word GJgets          one number from the stack        and prints   it;
     the word !SPACES! gets             one number from the      stack   and prints
     that many spaces;

     the word !EMIT! gets a number that           represents      a character          and
     prints that character;
     even the word STARS, which we defined      ourselves,                      gets     a
     number from the stack and prints that many stars.

When all operators   are defined     to work on the values that are
already   on the stack,  interaction      between  many operations
remains simple even when the program gets complex.
Earlier    we pointed   out that FORTH lets you execute   a word in
either of two ways: by simply naming it, or by putting     it in the
definition   of another word and naming that word. Postfix is part
of what makes this possible.             --
Just as an example,  let's suppose  we wanted a word that will
always add the number 4 to whatever  number is on the stack (for
no other purpose than to illustrate  our point).  Let's call the
word
     FOUR- MORE
We could define        it this   way:
     : FOUR-MORE 4 + ; Cii!lm)

and test     it this   way:
     3 FOUR-MORE.Cii!lm)~
and again:
     -10 FOUR-MORE,Cii!lm) -6 ok
The 11 4 11 inside the definition   goes onto the stack, just as it
would if it wete outside a definition.      Then the [3 adds the two
numbers on the stack.       Since [±I always works on the stack,   it
doesn't care that the "4" came from inside the definition    and the
three from outside.
As we begin to give some more complicated     examples, the value of
the stack and of postfix    arithmetic   will become increasingly
apparent  to you. The more operators   that are involved,   the more
important  it is that they all be able to "communicate"    with each
other,
24                                                                  Starting      FORTH




Keep Track      of Your Stack


We've just beg .un to demonstrate    the philosophy    behind the stack
and postfix    notation.   Before  we continue,     however,  let's   look
more closely    at the stack   in action   and get accustomed       to its
peculiarities.
FORTH's stack is described        as "last-in,   first-out" (LIFO). You can
see from the earlier     illustration       why this is so. The three was
pushed onto the stack first,          then the four pushed on top of it.
Later the adding machine          took the four off first    because it was
on top.  Hence "last-in,      first-out."
In general,  the only accessible       value at any given time is the
top value.     Let's     use another    cu>eration,   the GJto further
demonstrate.    Remember that each W removes one number from the
stack and prints     it.    Four dots, therefore,   remove four numbers
and print them.

        2 4 6 8 • • • .ll!Iim   8 6 4 2 ok




The system      reads   input   from left   to right     and executes          each   word
in turn.

        For input, the rightmost       value    on the    screen     will      end up on
        top of the stack.

        For output,  the rightmost      value   on the     screen     came from the
        bottom of the stack.

Let's     see what kind of trouble      we can get outselves          into.      Type:
        10 20 30 ••••

(that's    four dots)   then    RETURN. What you get        is:
1 FUNDAMENTALFORTH                                                              25




       10 20 30 • • . .cmmJ 30 20 10 0 • STACK EMPTYt

Each dot removes one value.                The fourth dot found that there was
no value left on the stack               to send to the terminal,   and it told
you so.




This error   is called    "stack           underflow."    (Notice   that   a stack
underflow  is not "ok. ")

The opposite       condition,          when the stack completely    fills up, is
called    "stack overflow.      11
                                       The stack is so deep, however, that this
condition      should never          occur except when you've done something
terribly    wrong.

It's important     to keep track of new words' "stack effects";  that
is, the sort of numbers a word needs to have on the stack before
you execute    it, and the sort of numbers it will leave on the stack
afterwards.

If you maintain    a list of your newly created      words with their
meanings as you go, you or anyone else can easily understand          the
words' operations.   In FORTH, such a list is called    a "glossary."

To communicate      stack effects   in a visual way, FORTH programmers
conventionally      use a special    stack notation    in their gl ossaries
or tables    of words.    We're introducing    the stack notation    now so
that you'll     have it under your belt when you begin            the next
chapter.




tFor   the Curious

Actually,  dot always prints whatever   is on the top, so if there is
nothing   on the stack, it prints whatever   is just below the stack,
which is usually     zero.  Only then is the error     detected;  the
offending    word (in this case dot) is returned      to the screen,
followed by the "error message."
26                                                          Starting   FORTH




Here's       the basic      form:

         (before   -     after)

The dash separates   the things that should be on the stack (before
you execute   the word) from the things    that will be left there
afterwards.    For example, here's the stack notation  for the word
G]:
                    (n --     )

(The letter    "n" stands for "number.")     This shows that G) expects
one number on the stack      (before)    and leaves   _!!.£ number on the
stack (after).

Here's       the stack      notation   for the word   [3.
         +             (nl n2 -- sum)
.When there     is more than one n, we number them nl, n2, n3, etc.,
consecutively.        The numbers l and 2 do not refer to position       on
the stack.     Stack position    is indicated   by the order in which the
 items are written;     the rightmost    item on either  side of the arrow
 is the topmost      item on the stack.       For example,    in the stack
 notation   of [±], the n2 is on top:

         +             (nl n2 -- sum)




                                           You're the top

Since you probably     have the hang of it by now, we'll be leaving
out thecmmI:)symbol     except where we feel it's needed for clarity.
You can usually      tell    where to press  "return"   because     the
computer's  response   is always underlined.
1 FUNDAMENTAL
           FORTH                                                                       27




Here's a list of the FORTH words you've lear ned so far, including
their stack notations   ( 11 n II stands for number; 11 c II stands for
character):

      XXX        yyy      --     )           Creates a new definition            with
                                             the name xxx, consisting              of
                                             word or words yyy.
  CR                      --     )           Performs a carriage  return         and
                                             line feed at your terminal.
  SPACES               (n --     )           Prints  the given   number of
                                             blank spaces at your termina l .
  SPACE                   -- )               Prints one blank space          at your
                                             terminal.
  EMIT                 (C --     )           Transmits   a character          to the
                                             output device.
   11
        xxx 11            --     )           Prints    the character         string
                                             xxx at your terminal.             The 11
                                             character      terminates           the
                                             string.
  +                    (nl n2 -- sum)        Adds.
                       (n --     )           Prints     a number,     followed       by
                                             one   space.



In the next chapter             we'll talk    about    getting      the   computer        to
perform some fancier           arithmetic.


Review of Terms

Compile                 to generate       a dictionary    entry in computer
                        memory from source text (the written-out        form
                        of a definition).      Distinct from "execute."
Dictionary              in FORTH, a list       of words and definitions
                        including       both     "system"      definitions
                        (predefined)   and "user" definitions       (which you
                        inven~.      A dictionary      resides   in computer
                        memory in compiled form.
28                                                          Starting     FORTH




Execute                to perform.   Specifically,    to execute       a word is
                       to perform   the operations       specified       in the
                       compiled definition     of the word.

Extensibility          a characteristic     of a computer language   which
                       allows    a programmer    to add new features     or
                       modify existing    ones.

Glossary               a list of words defined  in FORTH, showing their
                       stack effects  and an explanation   of what they
                       do,   which   serves    as a reference       for
                       programmers.

Infix     notation     the method of writing    operators   between           the
                       operands  they affect, as in "2 + 5."
Input     stream       the text to be read by the text interpreter.
                       This may be text that you have just typed in at
                       your terminal,  or it may be text that is stored
                       on disk.

Interpret              (when referring   to FORTH's text interpreter)     to
                       read the input stream,     then to find each word
                       in the dictionary    or, failing  that, to convert
                       it to a number.
LIFO                   (last-in,  first-out)   the type of stack   which
                       FORTH uses.      A can of tennis balls  is a LIFO
                       structure: the last ball you drop in is the one
                       you must remove first.
Postfix     notation   the method   of writing     operators   after the
                       operands they affect,   as in "2 5 +" for "2 + 5."
                       Also known as Reverse Polish Notation.

Stack                  in FORTH, a region      of memory       which   is
                       controlled   in such a way that     data   can be
                       stored or removed in a last-in, first - out (LIFO)
                       fashion.

Stack     overflow     the error condition    that occurs when the entire
                       area    of memory    allowed    for the   stack   is
                       completely  filled  with data.
Stack     underflow    the error    condition     that occurs          when    an
                       operation   expects    a value on the         stack,   but
                       there is no valid data on the stack.

Word                   in FORTH, the name of a definition.
1 FUNDAMENTAL
            FORTH                                                                           29




Problems          -   Chapter     1


Note:       before         you work these          problems,     remember       these   simple
rules:
              Every~           needs a Ii].
and
              Every        [:l needs      a [:f.


1.       Define a word called   GIFT which, when executed,   will                         type
         out the name of some gift.  For example, you might try:
                  : GIFT       . II BOOKENDSII
         Now define     a word called   GIVER which will print  out a
         person's  first name. Finally,   define a word called THANKS
         which includes    the new FORTH words GIFT and GIVER, and
         prints out a message something like this:
              DEAR STEPHANIE,
                 THANKSFOR THE BOOKENDS.ok


2.       Define       a word     called     TEN.LESS     which       takes   a number   on the
         stack,       subtracts teP,r and returns              the    answer   on the stack.
         (Hint:       you can use ~-)


3.       After entering  the words in Prob. 1, enter a new definition
         for GIVER to print someone else's name, then execute THANKS
         again.  Can you explain why THANKSstill prints out the first
         giver's name?
                                  2   HOW TO GET RESULTS


In this chapter,     we'll dive right into some specifics           that you
need to know before we go on. Specifically,           we '11 introduce some
of the arithmetic       instructions      besides   G and some special
operators   for rearranging       the order of numbers on the stack, so
that you'll be able to write mathematical         equations in FORTH.


FORTH Arithmetic              -- Calculator        Style

Here are          the    four     simplest       integer-arithmetic              operators       in
FORTH:t

.--------------                              - -----          -- -----~p~r_,onounced:
        +               (nl   n2 --   sum)                 Adds.
                        (nl   n2 --   diff)                Subtracts (nl-n2).
        *               (nl   n2 --   prod)                Multiplies.
        I               (nl   n2 --   quot)                Divides (nl/n2).

Unlike calculators, computer terminals   don't have
special  keys for multiplication     and division.
Instead we use ~ and [2].


tif     Math Is Not Your Thing
Don't worry if this chapter    looks a little like an algebra
textbook.  Solving math problems is only one of the things you
can do with FORTH. Later we'll explore some of the other things
FORTHcan do.
Meanwhile,   we'd              like   to remind         you that      integers      are      whole
numbers, such as:
        ... -3, -2, -1,       o, 1, 2, 3, ...
Integer arithmetic   (logically    enough) is arithmetic   that concerns
itself only with integers,     not with decimal-point    numbers, such as
2.71.



                                                   31
32                                                                Starting   FORTH




In the first chapter,    we learned  that we can add two numbers by
putting  them both on the stack, then executing    the word [±1,then
finally   executing   the word G) (dot) to get the result printed  at
our terminal.

     17 5 + . 22 ok

We can use this method with all of FORTH's arithmetic     operators.
In other   words,  we can use FORTH like     a calculator     to get
answers, even without writing  a "program. 11 Try a multiplication
problem:

     7 8 * . 56 ok

By now we've seen that the operator    comes after the numbers.  In
the case   of subtraction   and division,    though,  we must also
consider the order of numbers ("7 - 4" is not the same as "4 - 7").
Just remember         this   rule:

     To convert   to postfix,           simply   move the   operator    to the   end
     of the expression:


             Infix                     Postfix


             3   +4                    3   ...--:r-'+
             500 - 300                 500 ~-


             6 X5                      6~*


             20 / 4                    20~



So to do this         subtraction    problem:

     7 - 4 =

simply   type    in

     74-.~
2 HOWTO GET RESULTS                                                                                 33




          For Adventuresome         Newcomers          Sitting       at a Terminal



If you're one of those people who likes to fool around and figure
things   out for themselves    without    reading  the book, then you're
bound to discover    a couple of weird things.       First off, as we told
you, these operators    are integer     operators.   That not only means
that you can't do calculations      with decimal values, like

     10.00 2.25 +

it also    means that      you can only          get    integer      results,      as in

     21 4 / .~            instead      of     5.25 ok
Another     thing    is that    if you try       to multiply:

     10000 10 *

or some such large numbers, you'll     get a crazy answer.     So we're
telling  you up front    that with the operators    introduced   so far
and with G] to print the results,   you can't have any numbers that
are higher  than 32767 or lower than -32768.      Numbers within this




                      l
range are called   "single-length  signed numbers."



     +3276J               Allowable            range       of     single-length             signed
                          numbers.

     -32768~


Notice,   in the list of FORTH words a few pages back, the letter
"n," which stands for "number."       Since FORTH uses single-length
numbers more often than other types of numbers, the "n" signifies
that the number must be single-length.        And yes, there are other
operators    that extend   this range    ("double-length"   operators,
which are indicated    by "d ").

All of these        mysteries   will        be explained         in time,       so stay    tuned.
34                                                              Starting   FORTH




The order     of numbers      stays    the    same.     Let's   try   a division
problem:
     204/.~

The word [Z] is defined     to divide        the second    number on the stack
by the top number:




What do you do if         you   have    more     than     one   operator    in an
expession, like:
     4 + (17 * 12)

you ask? Let's take it step-by-step:             the parentheses       tell you to
first multiply seventeen  by twelve,            then add four.        So in FORTH
you would write:
     17 12 * 4 +     208 ok

and here's    why:
2 HOW TO GET RESULTS                                                    35




17 and 12 go onto   the   stack.   l!l multiplies    them and returns   the
result.




Then the four goes onto the stack, on top of the 204. [±I rolls         out
the adding machine and adds them together,     returning  only          the
result.
Or suppose   you want to add five     numbers.      You can do it in FORTH
like this:
36                                                 Starting    FORTH




      17 20 + 132 + 3 + 9 +.        181 ok

 17




 3




Now here's     an interesting      problem:
      (3+9)   * (4+6)
To solve it we have to add three to nine first, then add four to
six, then finally multiply the two sums. In FORTH, we can write
      3 9 + 4 6 + *     . 120 ok
and here's     what happens:




        '
        3
                                              6
                                              4
                                              12


Notice that we very conveniently     saved the sum twelve on the
stack while we went on about the business of adding four to six.
Remember that we're not concerned    yet with writing   definitions.
We are simply using FORTH as a calculator.
If you're like most beginners,   you probably would like to try your
hand at a few practice    problems until you feel more comfortable
with postfix.
 2 HOWTO GET RESULTS                                                                                        37




 Postfix      Practice            Problems                (Quizzie      2-a)


 Convert        the following                infix      equations         to postfix          "calculator
 style."        For example,

        ab+       C


 would become

        a b * C +



 1.     c(a + b)

 2.     3a - b         + C
            4
t3.     0.5 ab
          100
 4.     n + 1
          n
 5.     x(7x + 5)

 Convert        the following           postfix        expressions         to infix:

 6.     a b - b a + /

 7.     a b 10        */

 tFor   Beginners

 Remember,        we're       only      using        integer    arithmetic,             so you'll    have   to
 be clever.


                                  qo1                                      I ooz ,,. q e
                                   e      "L                   .lO     / Z / 001 ,,. q e            "€

                             e + q                                   +o/v-q,,.              e €     ·z
                            q--=---e ·9
                                                                                 ¥-   + q e o
           ¥- X       + £    ¥-   XL      '£                            .lO      ¥- 0   + q e       ·t
                      I u + t u           ·v               e-z a1zz1no                s.:i:a~suv
38                                                               Starting   FORTH




FORTH Arithmetic     -- Definition      Style

In Chap. 1 we saw that we could
define
numbers
words.
             new words
               and other
            Let's explore
possibilities,
newly-learned
                           in terms
                           pre-defined
                                       of
                            some further
                     using some of our
                   math operators.
                                                         •• W
                                                            m,•
Let's say we want to convert          various     measurements    to inches.        We
know that
      1 yard    36 inches
and
      1 foot=   12 inches
so we can define    these   two words:
          YARDS>IN 36 * ; ok
          FT>IN 12 * ; ck--
where the names symbolize     "yards-to-inches"                  and    "feet-to-
inches." Here's what they do:
      10 YARDS>IN• 360 ok
      2 FT>IN . 24 ok
If we always want our result         to be in inches,     we can define:
          YARDS 36 * ; ok
          FEET 12 * ; ~
          INCHES;~  --

so that    we can use the phrase
      10 YARDS2 FEET+ 9 INCHES+.                393 ok
Notice that the word INCHES doesn't    do anything    except remind
the human user what the nine is there for.     If we really  want to
get fancy, we can add these three definitions:
          YARD YARDS; ok
          FOOT FEET; ck°
          INCH;~    --

so that the user can enter the singular                  form of any of these
nouns and still get the same result:
2 HOW TO GET RESULTS                                                     39




      1 YARD 2 FEET + 1 INCH + • 61 ok
      2 YARDS 1 FOOT + • 84 ok

So far we have only defin e d words whose definitions             contain a
single math operator.         But it's perfec tl y possi b l e to put many
op e r a tors inside a defi ni t i on , if that's what you need to do.

Let's sa y we want a word that c omput es the sum of five numbe r s on
the stac k. A few pages back we summed five numbers like this:
      17 20 + 132 + 3 + 9 + . 181 ok
But we can also enter
      17 20 132 3 9 + + + +      181 ok
                                                       .      q
17                               132           5
                                       132
                                          20
                                                     3.
                                                    131              '
                                                                     3
                                          17                        132
                                                                    10
                                                                     17

[±]               [±)            EB
                                                              [J~
       12               14+
       132              20
       20               17
       17


We get the same answer, even though we've clustered      all the
numbers into one group and all the operators into another group.
We can write our defi nition like this:
      : 5#SUM     + + + + ; ok
and execute     it like this:
40                                                                                  Starting       FORTH




       17 20 132 3 9 5#SUM • 181 ok
If  we were going to keep 5#SUM for future use, we could enter it
into our ever-growing        glossary,   along   with a note that  it
"expects    five arguments"t       on the stack,   which it will add
together.
                                                                                    +
Here's        another     equation       to write       a definition        for:+

         (a   + b)   *C
As we saw in Quizzie                    2-a,     this     expression         can        be written       in
postfix as
       C      a b + *
Thus we could write                 our definition
         : SOLUTION           + *;      ok
as long as we make sure that                      we enter      the arguments            in the proper
order:

       c a b SOLUTION

tFor     Semantic        Freaks
In mathematics,              the      word "argument"             refers     to an independent
variable         o~ a function.                Computer      linguists       have       borrowed     this
term to refer to numbers being operated                                  on by operators.            They
have also borrowed the word "parameters"                                 to describe  pretty         much
the same thing.
tFor Beginners Who Like
     Word-problems
If a jet    plane    flies  at an
average air speed of 600 mph and
if it flies with a tail wind of 25
mph, how far will it travel     in
five hours?
If   we define
         : FLIGHT-DISTANCE                + *
we could enter
         5 600 25 FLIGHT-DISTANCE . 3125 ok

Try it with             different        values,        inc~uding         head     winds     (negative
values).
2 HOW TO GET RESULTS                                                                           41




Definition-style         Practice      Problems             (Quizzie     2-b)

Convert  the following  infix expressions    into FORTH definitions
and show the stack order required      by your definitions.      Since
this is Quizzie 2-b, you can name your definitions       2B1, 2B2, etc.
For example,


1.    ab+    C       would become               : 2B1     * + ;
      which expects        this     stack   order:      (c b a -    result)



2.    a - 4b       + C
        6

3.     a
     Sb
4.    0.5 ab
         100

5.    a(2a + 3)

6.    a - b
        C




                                                      ·l1:}Joqs lJah aonpoJ:}U1
11 1 aM qo1qM SlO:}eJado               uo1:}e1nd1uew       ~Oe:}s aq:} :}noq~1M
~sea1 ~e--j:}q6p   aJ,nol             'a1q1ssodw1    s,auo s1q:} p1es nol n                     •9

                                                                       (:}1nsal --      e e)
                                                              ,,. + £        ,,. c:    ss:c:    ·s
                                                                       (:}1nsaJ --      q e)
                                                                   ! I   ooc:..        vs:c:: ·v
                                                                       (:}1nsaJ -       q e)
                                                                       ! I   ,,. a     me: :    "£

                                                                   (Hnsa:i      -     q e o)
                                                               + I 9 - "' v            zs:c:    ·c:
42                                                                     Starting    FORTH




The Division       Operators


The word 12[is FORTH's simplest  division   operator.   Slash                     supplies
only the quotient; any remainder   is lost.   If you type:

       224/.~
you get only       the quotient         five,   not the remainder      two.

If you're        thinking      of a pocket   calculator's         per-cent
operator,       then five      is not the full answer.

But 12] is only one of several    division    operators  supplied      by
FORTH to give you the flexibility      to tell the computer    exactly
what you want it to do.

For example, let's say you want to solve this problem:        "How many
dollar   bills  can I get in exchange     for 22 quarters?"    The real
answer, of course,     is exactly  5, not S.S. A computerized     money
changer,    for example,   would not know how to give you 5.5 dollar
bills.

Here are two more FORTH division                  operators:


       /MOD         (ul u2 --                         Divides.   Returns
                        u-rem u-quot)                 the remainder
                                                      and quotient.
       MOD          (ul u2 -- u-rem)                  Returns the
                                                      remainder   from
                                                      division.


The "u" stands   for "unsigned."    We'll see what this~
means in the chapter    on computer  numbers.   For now ~
though, it means that the numbers can't be negative.     .

I/MODI gives both the remainder        and the quotient;  !MODIgives the
remainder    only.t      (For I/MODI, the stack notation    in the table
indicates   that the quotient     will be on the top of the stack, and
the remainder       below . Remember,     the rightmost  represents   the
topmost.)



tFor   the Curious

MOD refers          to   the     term     "modulo,"       which     basically       means
"remainder."
2 HOWTO GETRESULTS                                                                               43




 Let's try the first      one:
              22 4 /MOD • • 5 2    ok
 Here i/MODl performs the division   and puts both the quotient  and
 the remainder    on the stack.   The first dot prints the quotient
 because the quotient was on top.


~"ttuf(~JVMODI(i;IHh's                           older brother)

                                   I
                             .·
                             ·~sh~

 With what we've learned         so far, we can easily                     define   this word:
                                           11
     : QUARTERS         4 /MOD •       •        ONES AND    11
                                                                      II    QUARTERS II   ;




 So that     you can type:
      22 QUARTERS

 with this    result:
      22 QUARTERS 5 ONES AND 2 QUARTERS                          ok
 The second word in the table,                    iMOD!,   leaves      only     the remainder.
 For example in:
      22 4 MOD • 2 ok
 the two is the remainder.
44                                                                    Starting      FORTH




Stack Maneuvers

If you worked       Prob.   6 in the    last   set,    you discovered            that   the
infix    equation

        a - b
         C

cannot be solved with a definition                 unless     there   is some way to
rearrange values on the stack.
Well, there is a way:         by using     a "stack         manipulation       operator"
called !SWAPj:-

!SWAP!
The word !SWAP! is defined             to switch      the    order    of the      top   two
stack i terns:




As with the other stack manipulation          operators,                   you can test
!SWAP!at your terminal   in "calculator     style";   that                 is, it doesn't
have to be contained   within a definition.
2 HOW TO GET RESULTS                                                                                45




First    enter

        l 2 ••      2 l ok

then    again,      this    time with iSWAPj:
        1 2 SWAP • • 1 2 ok

Thus Prob.         6 can be solved           with this       phrase:

        - SWAP/

with    (c a b             ) on the stack.


Let's    give      a, b, and c these            test    values:
        a=    10           b = 4        C   =2
then    put them on the stack                and execute          the phrase,    like       so:

        2 10 4 - SWAP / .~




Here is a list         of several           stack      manipulation      operators,         including
iSWAPj.

        SWAP          (nl n2 -         n2 nl)                      Reverses       the top---=--
                                                                   two stack     items.

        DUP           (n -- n n)                                   Duplicates         the    top
                                                                   stack item.

        OVER          (nl n2 -         nl n2 nl)                   Makes    a copy     of
                                                                   the   second     item
                                                                   and pushes     it on
                                                                   top.

        ROT           (nl n2 n3 -- n~ n3 nl)                       Rotates   the third
                                                                   item to the top.
        DROP          (n --        )                               Discards    the          top
                                                                   stack item.
46                                                 Starting   FORTH




The next stack manipulation    operator on the list, IDUPI, simply
makes a second copy (duplicate) of the top stack item.




For example, if we have "a" on the stack, we can compute:
     a2

as follows:
     DUP *
in which the following    steps occur:

                 Contents
     Operation   -of -Stack
                        --
                 a

     DUP         a a
                 a2
     *
2 HOWTO GET-RESULTS                                                                          47




Now somebody              tells      you to evaluate           the expression:

        a * (a + b)

given        the following              stack     order:

         (ab    -     )

But, you say, I'm going to need a new manipulation     operator:       I
want two copies of the "a," and the "a" is under the "b."       Here's
the word you need:   loVERI. !OVER\ simply makes a copy of the "a"
and leapfrogs  it~     the "b":


         (ab    -- a~a)

Now the expression:

         a   * (a + b)
can easily          be written:

        OVER+ *

Here's       what happens:


                              Contents
        OEeration             of Stack

                                  a b

         OVER                     a b a

         +                        a (b+a)

         *                        a*(b+a)


When writing  equations  in FORTH, it's best to "factor                               them out"
first. For example, if somebody asks you to evaluate:

         a 2 + ab

in FORTH, you'll    find it quite   complicated                               (and maybe even
impossible)  using the words we've introduced                              so far .•. unless you
factor out the expression  to read:

         a * (a + b)

which        is the expression                  we just    evaluated   so easily.
48                                                  Starting   FORTH




The fourth stack manipulator on the list is !ROTi (uro ounced
rote), which is short for "rotate."
top three stack values:
                                                      1
                                      Here's what ROT does to the




For example, if we need to
evaluate the expression:
     ab - be
we should first      factor   out the "b"s:
     b   * (a - c)
Now if our starting-stack        order   is this:

     (c b a --

we can use:
     ROT - *
in which the following        steps   will occur:
2 HOWTO GET RESULTS                                                       49




                        Contents
     Operation          of Stack
                        ----
                        C   b a
     ROT                b a C
                        b (a-c)

         *               (b* (a-c))




The final stack manipulation    operator         on the list   is !DROPj. All
it does is discard the top stack value.




Pretty       simple,   huh?   We'll see some good uses for !DROP!later   on.
50                                                                      Starting   FORTH




                                         A Handy Hint
                                A Non-destructive       Stack   Print

Beginners   who are just learning      to manipulate numbers on the
stack in useful ways very often find themselves typing a series of
dots to see what's on the stack after their manipulations.      The
problem with dots, though, is that they don't leave the numbers
on the stack for future manipulations.
Here is the definition     of a very useful word for such beginners •
• sprints     out all the values   that happen   to be on the stack
"non-destructively";     that is, without removing them.    Type the
definition    in as shown here, and don't worry about how it works.
        : .S     CR 'S SO @ 2- DO I @ •                 -2 +LOOP ;~

Let's    test    it,    first     with nothing      on the stack:
        .s
        0 Ole

As you can see, in this version                     of .s, we always see at least one
number as a reference   for the                     bottom of the stack; that is, the
same    number         we see     when   we type    a   Q and get
        •cmmm'---o
              __ S_T_A_C_K_E_M_P_T_Y
Now let's       try it with numbers on the stack:
        1 2 3 .s
        0 1 2 3 ok
        ROT .S
        0 2 3 1 olc
2 HOWTO GET RESULTS                                                                                     51




Stack    Manipulation         and Math Definitions                             (Quizzie    2-c)


1.      Write a phrase which flips three                          items on the stack,             leaving
        the middle number in the middle;                         that is,
                a b C        becomes                 C   b a

2.      Write     a phrase         that     does         what    !OVER! does,          without      using
        jovERj.
3.      Write a definition  called                    <ROT, which         rotates  the top three
        stack items in the opposite                      direction      from [ROT!; that is,

                a b C        becomes                 C   a b


Write definitions            for      the      following         equations,        given      the   stack
effects shown:
4.      n + 1                (n -     result)
        ---
          n

5.      x(7x + 5)            (x --    result)

6.      9a 2 - ba            (a b -- result)




                              ,,. - dVM.S           ,,. 6 R:3:1\.O    9::>Z       ·9

                                     ! ,,. +    s     ,,. Lana        S:::>Z      ·s
                                      ! I avMs +1 ana                 v:::>Z
                        lO           ! I dVM.S + T ana                v::>Z       ·v
                                               ! .LOR .LOR           .LOR>        ·t
                                            dVM.S .LOR          ana dVMS          ·z
                                                                .LOR dVM.S        ·1

                                                o-z a1zz1no- sla~suv
52                                                                       Starting    FORTH




Playing      Doublest


The next      four   stack    manipulation       operators      should       look   vaguely
familiar:

     2SWAP      (dl d2 -- d2 dl)             Reverses     the    top
                                             two pairs     of   num-
                                             hers.

     2DUP       (d -- d d)                   Duplicates  the top
                                             pair of numbers.

     2OVER      (dl d2 -- dl d2 dl)          Makes   a copy   of
                                             the second pair of
                                             numbers and pushes
                                             it on top.

     2DROP      (d --   )                    Discards   the top
                                             pair of numbers.


                                                                           ~;
                                                                           ~
The prefix     "2" indicates       that these
stack manipulation       operators     handle
numbers in pairs. t The letter          "d" in
the stack    effects    column stands      for
 "double."      "Double"     has a special
significance     that we will discuss when
we discuss "n" and "u."

The "2"-manipulators           listed   above are
so straightforward,          we won't   even bore
you with examples.

One more thing:    there are still    some
stack manipulators    we haven't   talked
about yet, so don't go crazy by trying
too much fancy footwork on the stack.
                                                                   Guess            who.
tFORTH-79 " Standard

These     words are part of the Standard's               "Double Number Word Set,"
which     is optional in a Standard  system.              j2ROT! is included.
+
+ For   Old Hands

They can also        be used to handle        double-length       (32-bit)     numbers.
2 HOWTO GET RESULTS                                                                       53




Here's a list of the FORTH
                         words we've covered in this chapter:

 +               {nl n2 -       sum)   Adds.

                 {nl n2 -- diff)       Subtracts       (nl-n2).

 *               {nl n2 -- prod)       Multiplies.

 I               {nl n2 -- quot)       Divides       (nl/n2).

 /MOD            (ul u2 --             Divides.        Returns the
                    u-rem u-quot)      remainder        and quotient.

 MOD             (ul u2 - - u-rem)     Returns       the     remainder                from
                                       division.

 SWAP            (nl n2 -- n2 nl)      Reverses        the        top     two stack
                                       items.

 DUP             {n --   n n)          Duplicates            the         top      stack
                                       item.

 OVER            (nl n2 --             Makes a copy of the second
                    nl n2 nl)          item and pushes it on top.
 ROT             (nl n2 n3 --          Rotates        the     third            item      to
                                       the
                    n2 n3 nl)          top.
 DROP            (n --    )            Discards             the         top      stack
                                       item.

 2SWAP           (dl d2 -- d2 dl)      Reverses   the             top     two pairs
                                       of numbers.

 2DUP            (d -- d d)            Duplicates           the    top pairs             of
                                       numbers.

 2OVER           (dl d2 --             Makes a copy of the second
                    dl d2 dl)          pair of numbers and pushes
                                       it on top.

 2DROP           (d --    )            Discards         the        top         pair      of
                                       numbers.
54                                                Starting   FORTH




Review of Terms

Double-length
numbers           integers    which encompass a range of over -2
                  billion     to +2 billion     (and which we'll
                  introduce   officially in Chap. 7).

Single-length
numbers           integers  which fall within the range of -3276&
                  to +32767: the only numbers which are valid as
                  the arguments       or results   of any of the
                  operators    we've    discussed   so far.   (This
                  seemingly arbitrary     range comes from the way
                  computers are designed( as we'll see later on.)
2 HOWTO GETRESULTS                                                        55




Problems -- Chapter     2

(answers in the back of the book)



1.   What is the difference       between !DUPjjDUPjand j2DUPI?
2.   Write a phrase which will reverse         the order    of the top four
     items on the stack: that is,
           (l 2 3 4 -- 4 3 2 l)

3.   Write a definition  called 3DUP which will duplicate            the top
     three numbers on the stack: for example,
           (l 2 3 -   l 2 3 l 2 3)

Write definitions  for the following         infix   equations,   given   the
stack effects shown:

4.   a 2 + ab   +c      (c a b -- result)
5.   a - b              (a b -- result)
     a+b
6.   Write a set of words to compute prison        sentences              for
     hardened criminals such that the judge can enter:
           CONVICTED-OFARSONHOMICIDETAX-EVASIONok
           WILL-SERVE 35 YEARSok              --
     or any series  of crimes              beginning   with       the word
     CONVICTED-OF and ending              with WILL-SERVE.         Use these
     sentences:
           HOMICIDE               20 years
           ARSON                  10 years
           BOOKMAKING              2 years
           TAX- EVASION            5 years
7.   You're the inventory    programmer   at Maria's  Egg Ranch.
     Define a word called EGG.CARTONS   which expects on the stack
     the total number of eggs laid by the chickens      today and
     prints out the number of cartons that can be filled with a
     dozen each, as well as the number of left-over eggs.
                           3     THE EDITOR (AND STAFF)


Up till    now you've     been compiling    new definitions                     into the
dictionary     by typing      them at your terminal.        This                 chapter
introduces   an alternate    method, using disk storage.

Let's begin    with some observations                that   specifically   concern   the
dictionary.



Another   Look at the          Dictionary


If you've been experimenting     at a real                   live terminal,      you may
have discovered    some things  we haven't                   mentioned   yet.     In any
case, it's time to mention them.


  Discovery    One: You can define the same word more than once
  in different    ways--only the most recent definition  will be
  executed.

For example,     if you have        entered:
       : GREET      • " HELLO. I SPEAK FORTH. " ; ok

then   you should    get this      result:

       GREET HELLO.       I SPEAK FORTH. ok

and if you redefine:
       : GREET      • II HI THEREI II ;---2.!5_

you get the most recent           definition:
       GREET HI THERE! ok

Has the first    GREET been erased?       No, it's still   there, but the
most recent    GREET is executed    because of the search order.       The
text interpreter    always starts    at the "back of the dictionary"
where the most recent     entry is.    The definition    he finds first is
the one you defined last.      This is the one he shows to !EXECUTE!.



                                                57
58                                                             Starting    FORTH




We can prove that       the old GREET is still      there.   Try this:
       FORGETGREET ok
and
       GREET HELLO. I SPEAK FORTH. ok
(the old GREET again!)




The word !FORGET!looks up the given word in the dictionary      and,
in effect, removes it from the dictionar    along with anything you
may have defined since that word. FORGET, like the interpreter,
searches     starting   from the back; he only removes     the most
recently    defined version of the word (along with any words that
follow).      So now when you type GREET at the terminal,        the
interpreter    finds the original GREET.

!FORGET! is a good word to know; he helps you to weed out your
dictionary  so it won't overflow. (The dictionary takes up memory
space, so as with any other use of memory, you want to conserve
it.)

     Discovery Two: When you enter definitions     from the terminal
     (as you have been doing), your source text t is not saved.

Only the compiled        form of your definition         is saved     in the die-


tFor Beginners
The "source     text"   is the original   version     of the definition,      such
as:
        : FOUR-MORE 4 + ;
which the compiler       translates   into a dictionary      entry.
3 THE EDITOR (ANDSTAFF)                                          59




tionary.   So, what if you want to make a minor change to a word
you've already defined?   This is where the EDITOR comes in. With
the EDITOR, you can save your source text and modify it if you
want to.
The EDITOR stores your source text on disk.     So before we can
really discuss the EDITOR, we'd better introduce the disk and the
way the FORTHsystem uses it.


How FORTH Uses the Disk

Nearly all FORTH systems use disk memory.    Even though       disk
memory is not absolutely   necessary  for a FORTH system,       it' s
difficult to imagine FORTHwithout it.

To understand       what
disk memory does,
compare it with com-
puter memory (RAM).
The difference         is
analogous to the dif-
ference     between      a
filing  cabinet   and a
rolling card-index.
So far you've      been
using computer      mem-
ory, which is like the
card index.    The com-
puter can access this
memory almost instan-
taneously,     so pro-
grams that are stored
in RAM can run very
fast.   Unfortunately,
this kind of memory is
li mited    and rela-
tively expensive.

On the other hand, the disk is called    a "bulk memory" device
because, like a filing cabinet, it can store a lot of information
at a much cheaper price per unit of information   than the memory
inside the computer.
Both kinds of memory can be written   to and read from.
The compiler   compiles    all dictionary    entries  into computer
memory so that the definitions     will be quickly accessible.  The
60                                                        Starting     FORTH




perfect place to store source text, however, is on the disk, which
is what FORTH does.     You can either   send source text directly
from the keyboard  to the interpreter  (as you have been doing), or
you can save your source text on the disk and then later     read it
off the disk and send it to the text interpreter.


     SOURCE TEXT



                                                                   DICT-
                                                                   IONARY
                                                                     I\
                                                               (COMPUTE
                                                                   MEMOR'{)



                      DISK
                     MEMORY


Disk memory is divided          into units   called   "blocks."
Many professional        FORTH development     systems have 500
blocks     available     (250 from each disk drive).        Each
block holds 1,024 characters        of source text.    The 1,024
characters      are divided   for display   into 16 lines of 64
characters      each, to fit conveniently      on your terminal
screen.

       180   LIST

              0     LARGE LETTER-F>
              1     STAR    42 EMIT ;
              2     STARS    0 DO STAR LOOP;
              3     MARGIN    CR 30 SPACES;
              4     BLIP    MARGIN STAR;
              5     BAR    MARGIN 5 STARS;
              6     f    BAR BLIP BAR BLIP BLIP      CR
              7
              8
              9 f
             10
             11
             12
             13
             14
             15
3 THE EDITOR (AND STAFF)                                                       61




This is what a block looks like when it's          listed on your terminal.
To list a block for yourself, simply type         the block-number  and the
word !LISTI, as in:

       180 LIST

To give you a better    idea of how the disk is used, we'll assume
that your block 180 contains   the sample definitions   shown above.
Except for line 0, everything   should look familiar:  these are the
definitions you used to print a large letter   "F" at your terminal.

Now if you were to type:
       180 LOAD

you would send block 180 to the input stream and then on to the
text interpreter.        The text interpreter    does not care where his
text comes from.       Recognizing    the colons,    he will have all the
definitions    compiled.

Notice that we've put our new word F on line 9. We've done this
to show that when you load a block, you execute   its contents.
Simply by typing:

       180 LOAD

all the definitions    will        be compiled   and   a letter   "F"   will   be
printed at your terminal.
Now for the unfinished
business:         line     0.     The
words     inside     the paren-
theses are for humans only;
they are neither         compiled
nor executed.          The word [1j
(left parenthesis)        tells    the
text    interpreter         to skip
all the following           text up
to the terminating              r~ht
parenthesis.        Because W is
a word, it must be set off
with a space. t
It's good programming           practice   to identify   your application
blocks with comments,         so that fellow programmers    will understand
them.


tFor   Beginners

The closing    parenthesis   is not a word, it is simply a character
that is looked     for by [1), called a delimiter.   (Recall that the
delimiter   for [:] is the closing quote mark.)
62                                                                        Starting      FORTH




Here are a few additional         ways to make your blocks                 easy      to read:

     1.     Separate  the    name from the           contents      of a definition              by
            three spaces.

     2.     Break definitions      up into         phrases,     separated            by double
            spaces.
     3.     If the definition      takes         more than      one line,         indent    all
            but the first line.

     4.     Don't put more than            one     definition  on a single    line
            unless   the definitions             are very short   and logically
            related.

To summarize,   the      three    commands           we've      learned       so far       that
concern disk blocks      are:

     LIST        (n                Lists     a disk block.
     LOAD        (n                Loads a disk block
                                   (compiles or executes).
     ( XXX)           -- )         Causes the string xxx
                                   to be ignored by the text
                                   interpreter.    The character
                                   is the delimiter .
3 THE EDITOR (AND STAFF)                                                                                63




Dear EDITORt


Now you're       ready       to learn       how to put your text            on the disk.

First    find    an empty blockt             and list     it,   using     the form:
        180 LIST

When you list an empty block, you '11 see sixteen  line numbers (0 -
1~ running    down the side of the screen,   but nothing    on any of
the lines.   The "ok" on the last line is the signal    that the text
interpreter  has obeyed your command to list the block.

By listing a block,                   you also   select    that     block        as the     one you're
going to work on.



  180

                                                                         '{OUAREHE\\E
                                                                                    :
                 180

                 .------
                       --··-·-·-··.
                 ------·· ·· ·--
                 ......                                              CURI\ENT
                                                                        BLOCK.


                                                                        /80
                                                                  A "pointer"             in computer
                The terminal
                                                                  memory         (RAM).


Now that you've made a block                     "current,"       you can list             it by simply
typing the word
        L

Unlike ILISTI, [!!I does not want to be preceded                              by a block        number;
instead, it lists the current   block.


tFor    Those Whose EDITOR Doesn't                   Follow       These     Rules

The FORTH-79 Standard     does                   not specify        editor  commands.   Your
system   may use a different                      editor:    if     so, check  your system
documentation.

tFor    People      at Terminals

If you're using someone else's    system, ask them which blocks ate
available.    If you're using your own system, try 180. It should be
free (empty).
64                                                             Starting   FORTH




            L
                                                     YOUAREHERE:
             110




                                                   /80


Now that you have a current block, it's time to select    a current
line by using the word ['.fl. Suppose we want to write something on
line 3. Type:




                3T~====~

                t          """



[!] lets you selectthe current line.t  It also performs a carriage
return, then ~ the given line (which so far contains      nothing).
At the end of the line, it reminds you which line you're on:

       3 T
       A
                                                                          3   ok

(Remember, we're underlining the computer's output for the sake of
clarity.)  The caret at the beginning    of the line is the EDITOR's
cursor, which points to your current character     position. On your
terminal the caret might look like this:    f


tFor       the Curious
Actually,           the cursor position,  not the line   number, serves   as the
pointer.            More on this in a future footnote.
3 THE EDITOR (AND STAFF)                                                                              65




Now that your sights               are   fixed,          you can       put     some text        in the
current line by using            ~-

       P HERE IT ISmI!Jlm ok

[RIputs the string          that follows it (up to the carriage    return) on
the current   line.          It does not type out the line.     If you don't
believe  the string         is really  there, you can type:
       3 T
or simply:

       L
                toj
                a
                4
                       HI   IT   ,a
                 5
                 6
                 r
                ,
                8
                ,0
                II

                ,.
                IL
                /5
                ,,   01(




Remember that        your current             position       remains         the    same,   so if you
were   to now type

       P THERE IT WENTCiilml3 ok

followed by [!;],you'd           see that        the     latter     string         had replaced      the
former on line 3.

Similarly,    entering   [RIfollowed by at least two blank spaces (one
to separate     the [RIfrom the string,   the other as the string itself)
causes     the former string     to be replaced    by a blank space;     in
other words, it blanks the line.

In this chapter  the symbol              11     11
                                              )15  means     that   you type          a blank     space.
So to blank a line, type:
66                                                        Starting    FORTH




Character     Editing    Commands

In this section,        we'll   show you how to insert   and delete     text
within a line.




Before    you can insert    or delete     text, you must be able             to
position    the EDITOR's cursor       to the point  of insertion             or
deletion.    Suppose line 3 now contains:
     IF MUSIC BE THE FOO OF LOVE
and you want to insert the second "O" in "FOOD," you must first
position the cursor after the "FO" like this:
     IF MUSIC BE THE FOADOF LOVE
To position     the cursor,     use the command 00, followed   by a string,
as in
     F FOC!ll!ImJ

00searches   forward from the current position  of the cursor until
it finds the given string    (in this case "FO"), then places   the
cursor right after it.



     t°-
     AIF MUSIC BE THE FOO OF LOVE


                         ~
     IF MUSIC BE THE FOO OF LOVE

                         ~A
     IF MUSIC BE THE F;ffjOF         LOVE

If you don't know the starting  position of the cursor, first type
"3 T" to reset the cursor to the start of the line.   00 then types
the line, showing where the cursor is:
     IF MUSIC BE THE FOAD OF LOVE                                     3 ok
3 THE EDITOR (AND STAFF)                                                                   67




Nowthat the cursor is positioned where you want it, simply enter:
      I    ocmmm
and CT]will insert          the character      "O" just behind        the cursor.




      IF MUSIC BE

CT]then types        the corrected     line,    including     the cursor:
      IF MUSIC BE THE FOOAD OF LOVE                                                 3 ok




To erase a string (using the command ~), you must first                           find the
string, using I!]. For example,    if you want to erase                          the word
"MUSIC," first reset the cursor with:
      3 Tm;::mm

then type:
     F MUSicm;::mm
      IF MUSICABE THE FOOD OF LOVE                                                  3 ok

and then simply:


~   erases     the string     you just found with~-



      IF                       FOODOF LOVE

~ then       types   the line,    including    the cursor:
      IF A BE THE FOOD OF LOVE                                                      3 ok

The cursor       is now in a position           where       you can     insert   another
word:
68                                                                                Starting       FORTH




       IF   ROCKA BE THE FOOD OF LOVE                                                            3 ok




The command ~ finds       and deletes a string.                           It     is a combination
of [Kl and I!], giving  you two commands for                        the        price  of one.     For
example,  if your cursor is here:
       IF ROCKA BE THE FOOD OF LOVE

then      you can delete       "FOOD" by simply           typing:

       D FOODClIJ!Ilm
        IF ROCK BE THE A OF LOVE                                                                 3 ok

Once again,        you can     insert     text   at the    new cursor             position:

       I CHEESEBURGERSClIJ!Ilm
        IF ROCK BE THE CHEESEBURGERSA OF LOVE                                                    3 ok

Using @I is a little    more            dangerous       than        using         [El and     then      rn).
With the two-step    method,            you know      exactly        what         you're      going     to
erase before  you erase it.




The command [Bl replaces   a string  that   you've                             already       found.      It
is a combination  of 00]and [!]. For instance:

       F NEED AClIJ!Ilm
        COMPUTERS NEED AA TERMINAL                                                               2 ok
       R CAN BEClIJ!Ilm
        COMPUTERS CAN BEA TERMINAL                                                               2 ok

ffil is great          when you want        to make an insertion       in                  front   of     a
certain      string.       For example,       if your line O is missing                    an "E":

        ( SAMPLE DEFINITIONS)                                 MPTY                              0 ok

then it's   not easy to ~ your               way through  all those spaces to                          get
the cursor    over to the space              before  MPTY. Better   you should                         use
the following     method:

       F MPTYClIJ!Ilm

then

       R EMPTYClIJ!Ilm
3 THE EDITOR (AND STAFF)                                                                 69




ITILLIis the most powerful           command for deletion.     It deletes
everything       from the current   cursor position up till and including
the given      string.   For example, if you have the line:
BREVITY IS THE SOUL", THE ESSENCE, AND THE VERY SPARK OF WIT.

(note    the cursor         position),     then   the phrase:

        TILL SPARKmI!lmJ

or even just

        TILL KCIII!Jlm

(since    there's      only     one "K") will      produce

        BREVITY IS THE SOUL "OF WIT                                               5 ok

Has a nicer         ring,     doesn't    it?



The Find      Buffer        and the      Insert   Buffer


In order      to use the EDITOR effectively,                        you really  have to
understand      the workings of its "find                     buffer"   and its "insert
buffer."
You may not have known it,                 but when you typed

        F MUSICCIII!Jlm

the first       thing    [fl did was to move               the   string    "MUSIC" into
something         called    the "find    buffer."               A buffer,    in computer
parlance,      is a temporary    storage   place             for data.    The find buffer
is located      in computer memory (RAM).
70                                                                 Starting          FORTH




                                                      YOU AREHERE:
     F h\USIC                                       C.UR1'ENT    tu~P,EIITC.UMOP.
                                                     BLOC.I<.      Po&tnOIJ
                                                                                            t
                                                                  2.08
                                                        FIND    8 U FFEP.




 l                                                       M USIC



Then~       proceeded    to search   the line      for the contents         of the find
buffer.
Now you will be able         to understand      the fo l lowing variation                on [m:


that    is, ~ followed      immediately      by a return.
This variation  causes [mto search for the string that is already
in the find buffer, left over from the last time you used [m.


                                                        FIND BUFFER

                                                          MUSIC


tFor the Curious
By keeping the current   cursor position,   the editor doesn't   need
to keep a liepa)ate pointer   for the current line.    It simply uses
the word    MOD • Since there are 64 characters        per line, the
phrase
        208 64 /MOD • • 3 16 ok
shows the cursor        is located   at the 16th character         in line          3.
3 THE EDITOR (AND STAFF)                                                       71




Whatgood is this? It lets you find numerousoccurrences of the
same string without retyping        the    string.     For example,    suppose
line 8 contains the profundity:
       ATHEWISDOMOF THE FUTUREIS THE HOPE OF THE AGES

with the cursor at the beginning,         and you want to erase       the "THE"
near the end. Start by typing
       F THEJ51m!llm
       THE AWISDOMOF THE FUTURE IS THE HOPE OF THE AGES 8 ok
Now that "THE~ " is in the        find    buffer,    you can simply     type     a
series of single ~s:
       Flm!llm
       THE WISDOMOF THE AFUTUREIS THE HOPE OF THE AGES 8 ok
       Flm!llm
       THE WISDOMOF THE FUTURE IS THE AHOPEOF THE AGES 8 ok
etc., until you find     the   "THE" you want,        at which time you can
erase it with mJ.t
By the way, if you were to try entering
get:
                                                     rnone more time, you'd
       F TfIE NONE
This time !TIcannot    find a match for the find buffer,      so it
returns the word "THE" to you, with the error message "NONE."
Remember we said that [Q]is a combination              of [Kl and ~?      Well,
that means that @Ialso uses the find buffer.
With the cursor positioned   at the beginning           of the line and with
"THE):S" in the find buffer, you can delete             all the "THE"s with
single ~s:


                 OF THf FUTURE IS THE HOPE OF THE AGES                  8 ok

                 OF AFUTUREIS THE HOPE OF THE AGES                      8 ok

                 OF FU~URE IS AHOPEOF THE AGES                          8 ok

                 OF FUTURE IS HOPE OF AAGES                             8 ok


tFor    the Curious
mJ counts the number of characters in the find            buffer   and deletes
that many characters preceding the cursor.
72                                                                        Starting    FORTH




The other buffer       is called   the    II
                                               insert   buffer.     11
                                                                         It   is used by [!I.
Simply typing:
       Im:mlm
will insert    the contents   of the insert    buffer at the current
cursor position.    The following   experiment   will demonstrate how
you might use both buffers      at the same time.     Suppose line 14
contains
       "THE YONDER,THE DANUBE,AND THE MAX                                            14 ok
Now position      the cursor:
       F THE)SmI!Iim
        THE "YONDER,   THE DANUBE, AND THE MAX                                       14 ok
and insert:
       I BLUE~mI!Iim
       THE BLUE "YONDER,THE DANUBE,AND THE MAX                                       14 ok

You have now loaded        both buffers         like so:


                                          ~ f-:--FIND BUFFER
                                          ~THE
                                          ~ ~INSERT BUFFER

                                                 '--0 BLUEJ'
Now type:
       Ft:m!Ilm
       THE BLUE YONDER,THE "DANUBE, THE MAX                                          14 ok
and:

       rmmm
       THE BLUE YONDER,THE BLUE ~DANBUE,THE MAX                                      14 ok
and again:

                   IONDER, THE BLUE DANUBE,THE "MAX                                  14 ok
                   YONDER,THE BLUE DANUBE,THE BLUE "MAX 14 ok
This is what a computer scientist               would call        "spiffy."
3 THE EDITOR (AND STAFF)                                                        73




Line Editing Commands

Now that we've shown you how to move letters                and words around,
we'll show you how to move whole lines around.




The word ~, which we introduced        before, uses the very same
insert buffer that [!] uses. Assuming that you still have "BLUE" in
your insert buffer from the previous example and that line 14 is
still your current line, then typing:


will replace   the old line 14 with the contents     of the                insert
buffer, so that line 14 now contains only the single word:
     BLUE

To quickly       review,   you have now learned    three   ways to use [El:

     1) P ALL THIS TEXTC!II!'llm puts the string    in the insert
                                 buffer, then in the current line.
     2)   Pb~mml                          blanks the insert      buffer,     then
                                          blanks the current   line.
     3) PC!II!'llm                        puts the contents    of the      insert
                                          buffer in the current line.




A very   similar word is [ill. It places the contents  of the insert
buffer under the current line.      For example, suppose your block
contain~


             1 ADAMS
             2    BROWN
             3 CUDAHY
             4 DAVIS
             5 ELMER
             6
             7

             -                        -
74                                                                           Starting   FORTH




If you move your cursor               to line   2 with:

         2 T
          "BROWN                                                                        3 ok

and then        type:
         U CARLINGIII!lmJok
         U COOPERlliil!IiCJok

you'll      get:


     1 ADAMS
     2 BROWN
     3 CARLIN
     4   COOPER
     5   CUDAHY                                                             INSERT BUFFE~
     6   DAVIS
     7   ELMER
                                                                            COOPER
Inst e ad of replacing     the current line, [!!I squeezes the contents of
the insert   buffer in below the current     line, pushing all the lines
below it down.       If there were any t hing in line 15, it would roll
off and disappear .

It's easier  to use              rnJthan !IDwhen you're       adding       successive   lines.
For example:

         1 T P ADAMSlliil!IiCJ ok
         U BROWNlliil!IiCJ ok --
         U CUDAHYCIJimlD ok
         u oAvIS CIJimmoi<
         etc.               --

The three          ways of using       [m also apply      to [!!I.




IBJis the opposite of [!!I: it extracts the                   current   line.  Using the
above example, if you make line 3 current                      (with the phrase "3 T"),
then by entering:

         xmmm
you extract          line   3 and move the lower          lines      up.
3 THE EDITOR (AND STAFF)                                           75




  1 ADAMS
  2 BROWN                                           INSE~T l?,UFFEf\
  3 COOPER
  4 CUDAHY
  5 DAVIS                                           CARLIN
  6 ELMER




As you see, IBJalso moves the extracted     line into the insert
buffer.  This makes it easy to move the extracted   line anywhere
you want it. For example, the combination:
       9 TIJii!IMJ

and:
       PIJii!IMJ

would now put "CARLIN" on line 9.


Miscellaneous        EDITOR Comands

iWIPEI
The word iWIPEI blanks an entire   block.      You can use IWIPEI to
ensure that there will not be any strange     characters which might
keep a block from being loaded.
If your system doesn't have IWIPEi, another   way to blank an entire
block is this:  first enter
       0 Ttiii!!ml

then hit
       X

sixteen    times.
76                                                                Starting        FORTH




~ and     [ID
When you type the word                ffil, you
add one to the current                 block
number.
Thus the combination:
       N L
                                                             1+
                                                  !iii
                                                              ~,a,
                                                                                    CURI\E
                                                         ~            CUl\1\ENT
                                                  ~ r7
                                                                                    CUii.SOil
                                                                       &LOC.I<
causes       the     next     block    to   be
listed.
                                                                  l
Similarly,         the word~    subtracts
one from            the current    block
number.                                                               YOUAREHERE:
Thus the combination:                              fDl
                                                   ~r-r~     1-       CUP.P.ENT


       B L                                                    ~,soI
                                                                       &LOC.K




lets   you list      one block back.                              !




We can't say too much about this word until we discuss how the
FORTH "operating  system" converses with the disk, but for now you
should know this:    !FLUSHlt assures you that any change you've
made to a block really gets written to the disk.
Say you've made some changes           to a block,
then you turn off the computer.           When you
come back tomorrow and list the block, it
may seem as though          you never made the
changes      at all.     The operating     system
simply didn't       get around to writing       the
corrected      block to the disk before         you
turned off the computer.         The same thing
could     happen     if you were to load your
application       and then crash       the system
before it could write the changes to disk.

tF ORTH-79 Standard
In the Standard,            the name for this     word is !SAVE-BUFFERS!.
3 THE EDITOR (AND STAFF)                                                             77




So always enter !FLUSH! before removing the disk, cycling    power,
 r tr~ing  something dangerous.    Some programmers    habitually
1
FLUSH after every change without even thinking about it.


iCOPYi

The word !COPY! lets you           rn      one block to another,    displacing
whatever was in the destination             block.  You use it in this form:
      from to    COPY

For example,     entering:
      153 200 COPY

will copy whatever         is in block 153 into      block 200.
Make it a habit     to !FLUSH!after         every   iCOPYj.




~ is an expanded      version   of        m.
                                         It lets you search for a given
string    in and beyond      your current     block into the following
blocks,   up to the block that you specify.
For   example,   if your     current    block   is 180, and   you type;

      185 S TREASURE

then ~ will search for "TREASURE" in blocks 180 thru                      184.   If it
finds "TREASURE" in, say, block 183, it will type:

      THIS MOMENT
                THAT WE TREASUREATOGETHER                                 7 183 ok

giving    both the block       and the line     number.
The block number with which you precede      the word [ID represents
the next block after the · last one you want searched.    There is a
reason for this, but it won't make sense until a later chapter.
78                                                        Starting   FORTH




[Bl lets you move an individual  line (or group of lines) from one
block to another.    To move a line to another   block, first make
the line current with
       182 LIST
then
       7 T
        AI SHOT A LINE INTO THE AIR                                  7   ok
Then enter the destination            block and the number of the line
under which you want the line         inserted, followed by the word IB]:
190 2 M




                                                    /90




           182.


           7 I SHOTA LINE wroTHE"'"




The line of text in the current         block (block 182) moves down to
the next line.  So to move three        consecutive lines, simply enter
       190 2 MmI!ImJ
       190 3 MmI!ImJ
       190 4 Mcm!Jlm
3 THE EDITOR (AND STAFF)                                              79




Youcan type the caret character instead of RETURN
                                               to indicate
the end of a character      string, so that you can get more than one
command on a line.
For example,     you could type:
       D FRUITA I NUTSC!Ii!ll'm
all on the same line,     and get the same result   as if you had typed:
       D FRUITC!Ii!ll'm

and:
       I NUTSC!Ii!ll'm


That's it for the EDITOR commands.     Because FORTH is naturally
flexible, and because users can define their own EDITOR commands
if they want to, the set of EDITOR commands in your system may
vary from the set presented    here.  This chapter closes with a
review of all the commands we've talked about.
One final observation    about the EDITOR: it is not a program, as
it might be in another     language.    It is rather   a collection    of
words.   The EDITOR, in fact, is called       a "vocabulary."       We'll
discuss the significance   of vocabularies   in a later chapter.


Getting    [ii5Xoled

Now that you've learned    to edit your definitions   into a block,
it's time to load them. But consider for a inoment: each time you
load definitions, you increase the size of your dictionary.
For example, let's say you write a definition    for something you
call !FUNCTION, edit it into an available  block, and load it. You
test it and realize  you forgot a ISWAPj. So you fix the source
text with the EDITOR commands, then load the block again.       It
works!
Now in the same block you edit in a definition    of something you
call 2FUNCTION and load the block again.     This time, you get it
right on the first try.  But what does your dictionary   look like?
From loading this block three times, you've got three versions of
!FUNCTION in there.   The simplest way to avoid this problem is to
use the word
80                                                                    Starting   FORTH




        EMPTY

jEMPTYI       "forgets"       all   the
definitions        that  you yourself
have      defined       (not    s stem
definitions).
at the beginning
                  t If you put EMPTY!
                         of the block,
                                      1                           SYSTEM

you will start with a clean slate                             DE'FINITIONS
each time you load.

For example:



        0       SOLUTIONS           QUIZZIE 2-B>             EMPTY
        1       2B1   * +
        2       2B2      4   * -    6 /   +;
        3




Sometimes you don't want to get rid of your whole application,
only part of it.        Suppose you were to write a word processing
application      (so you can enter text, edit it in memory, then output
it to a printer).       After you've finished     the basic    application,
you want to add variations,              so it can use one format           for
correspondence,         another    format   for magazine    articles,       and
another     format for address   labels.

                                          DICTIONAlW
                                            SYSTEM
                                           DEFINITIONS

                                            WOP.I)
                                           PROCESSING
                                           APPLICATION


                                                            LABEL
                                                            FDRM~T



 tFor       People    on a Multiprogrammed         System
 IEMPTY! "forgets"           your   own personal      extension     of the   dictionary,
 not anyone else's.
3 THE EDITOR (ANDSTAFF)                                               81




In FORTH these three variations     are called "overlays"  because
they are mutually exclusive     and can be made to replace    each
other.  Here's how.
The basic word processing  application  should begin       with !EMPTY!.
The last definition should be a name only, such as
       : VARIATIONS
This is called  a "null definition"  because it does       nothing    but
mark a place in your portion of the dictionary.
Then at the    beginning    of each   variation   block,   include   the
expression
       FORGETVARIATIONS                   VARIATIONS;

Now when you load one variation,          it
!FORGET!s back to the null definition,
compiles     a new null definition,     and
then     compiles      the  variation's
definitions.      When you load the other
variation,   you replace the first overlay
with the second overlay.
One more trick:   what if the source text for your application
takes more than one block?    The best solution is to let one block
load the other blocks.     For example, your "load block" might
contain:




      0 ( MY APPLIC HION>
      1
      2 180 LOAD                  182 LOAD
      -                                                              --
It's much better to let a single load block !LOAD)all the related
blocks than to let each block load the next one 1n a chain.
Now you know the ropes of disk storage.    You'11 probably want to
edit most of the remaining    examples and problems in this book
into disk blocks rather  than straight  from the keyboard to the
interpreter,  especially  the longer ones.   It's just easier that
way.
82                                                               Starting     FORTH




                 A Handy Hint -      When a Block Won't [IiOA5I

On some FORTH systems,    the following  scenario     may sometimes
happen to you: you load some new definitions       from a block, but
when you try to execute    them, FORTH doesn't   seem to have ever
heard of them (responding with a "?").
First you want to check whether any or all of your definitions
were actually     compiled into the dictionary. To do this, enter an
apostrophe    followed by a space, then the name of the word, then
a G], as in
       I    THINGAMAJIG.mi!ml

If GJprints   a number,       then    the   definition      is compiled,      but if
FORTH responds
       THINGAMAJIG?
then it isn't. There are two possible             reasons    for part   of a block
not getting compiled:

1) You made a typing error that keeps FORTH from being                       able   to
recognize a word. For instance, you may have typed
       (COMMENTLINE)
without a space after U]. This type of error is easy to find and
correct     because    FORTH prints the name of any word it doesn't
understand,     like this:
       180 LOADmi!mJ     (COMMENT?
2) There  is a non-printing       character    (one            you can't       see)t
somewhere in the block.     To find a non-printing              character,      enter
this:
       0    TmI!mJ
       1 Ttlm:lm
       2 Ttlm:lm       etc.
If a line contains  any non-printing      characters,     the "ok" at the
end of the line will not line up with the "ok"s at the ends of
the other lines,   because  non-printing       characters     don't print
spaces.  For any such line, reenter    the entire line (using IR]).

tFor       Experts
The "null"   character    (ASCII 0) is the culprit.   On most FORTH
systems, null is actually   a defined word, synonymous with !EXIT!, a
word we will discuss in Chap. 9.
3 THE EDITOR (AND STAFF)                                                 83




                              A Handy Hint

               A Better   Non-destructive     Stack   Print


Now that you know how to load longer          definitions      from a disk
block,   here's   an improved    version   of .S which      displays   the
contents    of the stack non-destructively     without    displaying    the
"stack-empty"    number.

This version uses an additional    word called   DEPTH, which       returns
the number of values on the stack.     (Follow it with G].)t

If you're   a beginner,     you might   want to enter          these  two
definitions  into a special    block all by themselves         so you can
load them any time you want them.


                0     NON-DESTRUCTIVE STACK PRINT)
                1
                2     DEPTH   S0@  'S - 2/ 2-   ;
                3     .s   CR DEPTH IF
                4        'S S0@ 4     -
                                     DO I (?  -2 +LOOP
               5             ELSE " Empty " THEN
               6
               7




t FORTH-79 Standard
The Standard   word set   includes   [i5E'P'Tiij.
84                                                                            Starting     FORTH




Here's        a list   of the FORTH words we've covered                   in this    chapter:


     LIST                  (n --                            Lists    a disk block.
     LOAD                  (n --                            Loads a disk block           (compiles
                                                            or executes).
     ( XXX)                ( --      )                      Causes the string    xxx to be
                                                            ignored    by the text inter-
                                                            preter.    The character   ) is
                                                            the delimiter.

     FLUSH                 ( --      )                      Forces    any modifications
                                                            that   have been made to a
                                                            block to be written to disk.

     COPY                  (source       dest - -       )   Copies     the contents         of the
                                                            source     block to the         desti-
                                                            nation    block.
     WIPE                                                   Sets the contents      of the
                                                            current block to blanks.
     FORGET xxx                                             Forgets all definitions             back
                                                            to and including   xxx.

     EMPTY                 (   --    )                      Forgets  the entire    contents
                                                            of the user's dictionary.

Editing         Commands -      Line Operators
     T                     (n --                            ~ the         line.

                           (   -                            Copies the given string,      if
                  or                                        any, into the insert  buffer,
                                                            then puts a copy of the in-
                                                            sert buffer  in the current
                                                            line.

     u                     (   -- )                         Copies the given string,
                                                            any, into the insert   buffer,
                                                                                           if
     u)S'~        or
     U XXX                                                  then puts a copy of the in-
                                                            sert buffer in the line under
                                                            the current line.        ---

     M                     (block line        --    )       Copies the current       line into
                                                            the insert     buffer,  and moves
                                                            a copy of the insert         buffer
                                                            into the line under the spe-
                                                            cified    line     in the desti-
                                                            nation block.
3 THE EDITOR (AND STAFF)                                                      85




  X                   (   --   )               Copies the current   line into
                                               the insert   buffer    and ex-
                                               tracts   the line   from the
                                               block.
Editing      Commands -- String    Operators
  F         or        (   --   )               Copies the given string,   if
  F XXX                                        any, into the find buffer,
                                               then finds the string in the
                                               current block.
  S         or        (n --    )               Copies the given string,       if
  S XXX                                        any, into the find buffer,
                                               then searches      the range of
                                               blocks,   starting     from the
                                               current    block    and ending
                                               with n-1, for the string.
  E                   (   --   )               To be used after F. Erases
                                               as many characters        as are
                                               currently    in the find buffer,
                                               going     backwards    from the
                                               cursor.
  D         or        (   --   )               Copies the given string,     if
  D XXX                                        any, into the find buffer,
                                               finds the next occurrence   of
                                               the string within the current
                                               line, and deletes it.
  TILL     or         (   -- )                 Copies the given string,        if
  TILL XXX                                     any, into the find buffer,
                                               then deletes    all characters
                                               starting   from the current
                                               cursor position     up till   and
                                               including the string.--
  I         or        (   -- )                 Copies the given string,       if
  I   XXX                                      any, into the insert   buffer,
                                               then inserts  the contents    of
                                               the insert    buffer   at the
                                               point just behind the cursor.
  R         or        (   --   )               Combines the commands E and
  R XXX                                        I to replace   a found string
                                               with a given string     or the
                                               contents     of the   insert
                                               buffer.
  i or ~              (   --   )               Indicates      the end of the
                                               string    to   be placed  in a
                                               buffer.
86                                                            Starting      FORTH




Review    of Terms

Block                in FORTH, a division        of disk memory containing
                     up to 1024 characters       of source text.
Buffer               a temporary    storage    ;rea   for data.
Disk                 a disk that has been coated   with a magnetic
                     material   so that, as in a tape recorder,    a
                     "head" can write or read data on its surface as
                     the disk spins.
EDITOR               a vocabulary  which allows         a user      to enter     and
                     modify text on the disk.
Find buffer          in FORTH's EDITOR, a memory location      in which
                     the strin,.i that is to be searched for is stored.
                     Used by l!'.], ~, [QI,ITILLI, and ~-
Insert    Buffer     in FORTH's EDITOR, a memory location      in which
                     the stri~    that is to be inserted     is stored.
                     Used by l.!J, ~, and I!!]. In addition,   ~ moves
                     the line that it deletes into the insert buffer.
Load block           one block which, when loaded, itself                loads   the
                     rest of the blocks for an application.
Null Definition      a definition    that     does nothing,       written   in the
                     form:
                            NAME;
                     that is, a name only will be compiled into the
                     dictionary.    A null definition    serves as a
                     "bookmark" in the dictionary,    for !FORGET! to
                     find.
Overlay              a portion      of an application             which,   when
                     loaded,     replac~s   another           portion    in the
                     dictionary.
Pointer              a location   in memory where a number can be
                     stored (or changed) as a reference to something
                     else,
Source text          in FORTH, the written-out    form of a definition
                     or definitions     in English-like     words and
                     punct~ation,   as opposed to the compiled       form
                     that is entered into the dictionary.
3 THE EDITOR (AND STAFF)                                                 87




Problems -- Chapter 3


1.   a)   Enter your definitions of GIFT, GIVER and THANKS from
          Probs. 1 and 3 of Chap. 1 into a block,  then load and
          execute THANKS.

     b)   Using the EDITOR, change       the person's        name in the
          definition  of GIVER, then load and execute        THANKS again.
          What happens this time?


2.   Try loading  some of your mathematical         definitions  from Chap.
     2 into an available  block, then load    it.      Fool around.
                      4   DECISIONS, DECISIONS, ...


In this chapter we'll learn how to program the computer to make
"decisions."   This is the moment when you turn your computer into
something more than an ordinary calculator.


The Conditional     Phrase

Let's see how to write a simple decision-making     statement     in
FORTH. Imagine we are programming      a mechanical    egg-carton
packer.  Some sort of mechanical device has counted the eggs on
the conveyor  belt, and now we have the number of eggs on the
stack.  The FORTHphrase:
     12 = IF      FILL- CARTON THEN
tests whether the number on the stack is equal to 12, and if it is,
the word FILL-CARTON is executed.    If it's not, execution  moves
right along to the words that follow !THEN!.




The word G takes two                     and compares them to see
values off the stack                     whether they are equal.




                                    89
90                                                                Starting    FORTH




-~                   FILL-CARTON
                            ITHENL_If~_         ~
If the condition         is true,                 But if the condition     is
[g:] allows the flow of                           false, [g:] causes the flow
execution       to continue with                  of execution     to skip to
the next       word in the definition.            !THEN!, from which          point
                                                  execution    will proceed.

Let's    try   it.    Define   this   example   word:
        : ?FULL 12 = IF ." IT'S FULL " THEN ; ok
        11 ?FULL ok
        12 ?FULLIT'S FULL ok

Notice:     an [g:]•.. !THEN!statement   must be contained           within a colon
definition.       You can't     just enter   these  words          in "calculator
style."

Don't be misled~the         traditional     English meanings of the FORTH
words (!fil and ~-         The words that follow        IF are executed   if
the condition     is true.    The words that follow        THEN are always
executed,    as though you were telling           the computer, "After you
make the choice,     then continue      with the rest of the definition."
(In this example, the only word after !THEN! is @, which ends the
definition.)

Let's look at another    example.     This definition   checks whether
the temperature   of a laboratory    boiler is too hot.    It expects to
find the temperature   on the stack:
        : ?TOO-HOT        220 > IF • " DANGER-          REDUCE HEAT " THEN ; ok
If the temperature    on the stack is greater    than 220, the danger
message will be printed     at the terminal.    You can execute   this
one yourself,   by entering   the definition, then typing   in a value
just before the word.
        290 ?TOO-HOT DANGER-             REDUCE HEAT ok
        130 ?TOO-HOT ok
4 DECISIONS, DECISIONS, .•.                                                         91




Remember that every [!!I needs a ITHENI                        I NOWPRONOUNCE'
to come home to. Both words must be in                         YOUIlEJ
                                                                     ANDCTBrBJ.
the same definition.

Here is a partial    list of comparison
2£.erators that you can use before an
~ ... ITHENIstatement:




     <

     >



     O=
     0<

     0>


The words @ and 0 expect         the same stack        order     as the    arithmetic
operators, that is:

     Infix                                   Postfix

     2 < 10     is equivalent    to          2   'la'<
                                                 ~
     17 > -39   is equivalent    to          17 -39       >


The words [23, IQ3), and [Q:g expect         only   one       value    on the   stack .
The value is compared with zero.

Another   word, INOTI, doesn't         test  any value at             all;   it simply
reverses   whatever condition         has just been tested.               For example,
the phrase:
     ••• = NOT IF

will execute   the words after        ~.   if the   two numbers on the stack
are not equal.
92                                                          Starting        FORTH




The Alternative      Phrase


FORTH allows   you to provide    an alternative           phrase       in   an   [gJ
statement, with the word !ELSEI.
The following   example        is a definition    which    tests     whether      a
given number is a valid       day of the month:
        ?DAY      32 < IF • " LOOKS GOOD "   ELSE • " NO WAY II THEN :

If the number on the stack is less than thirty-two,  the message
"LOOKS GOOD" will be printed.     Otherwise,    "NO WAY" will be
printed.




                                             GOOD"

                                     "NO WAV"


Imagine that [IT] pulls a railroad-track      switch, depending  on the
outcome of the test.    Execution    then takes one of two routes,   but
either way, the tracks rejoin at the word !THENI.
By the way, in computer      terminology,         this whole       business      of
rerouting the path of execution    is called       "branching.     nt

Here's a more useful example.     You know that dividing  any number
by zero is impossible,    so if you try it on a computer,  you'll get
an incorrect    answer.  We might define  a word which only performs
division     if the denominator      is not zero.     The following
definition   expects stack items in this order:




tFor   Old Hands

FORTH has no GOTO statement.  If you think you can't  live without
GOTO, just wait. By the end of this book you'll   be telling   your
GOTO where to GOTO.
4 DECISIONS, DECISIONS, •••                                                                 93




         (numerator denominator           -    )

         : /CHECK       DUP O= IF • II INVALID II          DROP
                          ELSE / THEN : t


Notice      that     we first    have     to !DUP! the        denominator    because       the
phrase
        O= IF
will     destroy     it in the process.

Also notice    that the word !DROP! removes    the denominator    if
division  won't be performed,  so that whether    we divide  or not,
the stack effect will be the same.



Nested      [IF]... [Tii'E'Nj
                            Statements


It's  possible      to put an____[g]••. THEN (or I!!] ... !ELSEj ••• jTHEN!)
statement    inside   another   ~-    THEN statement.    In fact, you can
~s        complicated      as you like, so long as every [fl has one
~-
Consider   the following            definition,     which determines   the size             of
commercial    eggs (extra          large,    large,  etc.), given their weight              in
ounces     per     dozen:


            EGGSIZE          DUP 18 < IF            .. REJ'ECT....           ELSE

                                                    "MEDIUM ..
                             DUP 21 < IF            "SMALL                   ELS~
                             DUP 24 < IF
                             DUP 27 < IF                        ..
                                                    .. EXTRA LARGE .. ELSE
                                                    "LARGE
                                                                             ELSE
                                                                             ELSE
                             DUP 30 < IF
                                                    " ERROR     ..                     +
                                                                                       +
                                   THEN THEN THEN THEN THEN DROP




tFor     Experts

There     are better        ways to do this,        as we' 11 see.

fFor     People     at Terminals
Because this definition                 is fairly     long,     we suggest    you load       it
from a disk block.
94                                                                          Starting       FORTH




Once EGGSIZE has been               loaded,   here    are some results           you'd    get:

       23 EGGSIZE MEDIUM ok
       29 EGGSIZE EXTRA LARGE ok
       40 EGGSIZE ERROR ok t


We'd like       to point     out a few things         about   EGGSIZE:

The entire     definition       is a series   of "nested"     @ ... jTHENI
statements.    The word "nested"        does not refer   to the fact that
we 're deaiing   with eggs, but to the fact that the statements       nest
inside one another,       like a set of mixing bowls.

The five LTHENls at the              bottom   close     off   the   five     ~sin         reverse
order; that is:


       IF----




                                    THEN THEN


Also notice     that  a !DROP! is necessary                         at     the      end   of     the
definition  to get rid of the original  value.

Finally,  notice           that the definition     is visually     organized    to be
read easily     by         human beings.       Most FORTH programmers          would
rather   waste   a         little  space    in a block    (there     are plenty    of
blocks) than let            things get any more confused        than they have to
be.




tFor   Trivia     Buffs

Here is the official           table     on which     this    definition         is based:

       Extra Large          27-30
       Large                24-27
       Medium               21-24
       Small                18-21
4 DECISIONS, DECISIONS, ...                                                                      95




A Closer Look at [rFj


Howdoes the comparison operator
([3, 8], [B, or whichever)     let ~
know whether the condition      is true
or false?   By simply leaving     a one
or a zero on the stack.          A one
means that the condition      is true;
a zero means that the condition       is
false.

In computer jargon,    when one piece of program                          leaves a value          as
a signal   for another   piece  of program, that                         value is called           a
"flag."

Try entering   the following                phrases    at      the   terminal,       letting      G]
show you what's on the stack                as a flag.

       5 4 > • l ok
       5 4 < •""""'o'ok

(It's okay to use comparison        operators  directly    at your terminal
like this,     but remember    that   an ~ ... jTHENi statement      must be
wholly     contained    within    a definition      because    it involves
branching.)

rm  will take a one as a flag that means true and a zero as a flag
that means false.    Now let's  take a closer look at JNOTI, which
reverses    the   flag     on the     stack.

       0 NOT . l ok
       l NOT .Dok

Now we '11 let           you in on a little    secret:   [!]:] will take                       ~
non-zero  value          to mean true.t   So what, you ask?    Well, the                       fact



tFor   the Doubting        Few

Just to prove      it,    try    entering      this   test:
       : TEST     IF • II NON-ZERO II ELSE • II ZERO II THEN                     t
Even though    there    is no comparison   operator  in the                               above
definition, you'll still get      0 TEST ZERO ok
                                  l TEST NON ZERO ok
                                  -400 TEST NON ZERO ok

!For Memory-Misers              Who Read the above            Footnote

       : TEST     IF . " NON-"          THEN • " ZERO "
96                                                                   Starting   FORTH




that an arithmetic   zero is identical            to a flag   that     means "false   11


leads to some interesting   results.
For one thing,    if all you want to test is whether  a number is
zero, you don't need a comparison operator   at all. For example,
a slightly simpler version of /CHECK, which we saw earlier, could
be
        : /CHECK     DUP IF /     ELSE • " INVALID II DROP THEN

Here's another   interesting result. Say
you want to test whether a number is an
even multiple of ten, such as 10, 20, 30,
40, etc.  You know that the phrase
        10 MOD
divides    by ten  and returns      the
remainder   only. An even multiple     of
ten would produce a zero remainder,    so
the phrase
        10 MOD O=
gives    the appropriate       "true"     or "false"
flag.
If you think about it, both~       and !NOT! do exactly  the                     same
thing:   they change zeros to on-es and non-zeros to zeros.                      They
have different   names because one makes more sense dealing                       with
numbers, the other with flags.
Still another interesting     result is that you
can use E] (minus) as a comparison operator
which tests   whether     two values   are "not
equal."     When you subtract        two equal
numbers,   you get zero (false):       when you
subtract   two unequal      numbers,  you get a
non-zero value (true).
And a final      result    is described     in the next
section.
4 DECISIONS, DECISIONS, •••                                                       97




A Little    Logic

It's possible   to take several    flags from various tests and combine
them into a single     flag for one [rn statement.     You might combine
them as an "either/or"           decision,    in which     you make two
comparison    tests.   If either   or both of the tests     are true, then
the computer will execute something.        If neither  is true, it won't.


Here's   a rather    simple-minded
example,   just to show you what
we mean.    Say you want to print
the name "ARTICHOKE"            if an


                                                                   -
input number is either       negative
~ a multiple    of ten.


How do you do this        in   FORTH?
Consider the phrase:

        DUP 0<   SWAP 10 MOD 0= +

Here's  what happens    when        the
input number is, say, 30:

                    Contents
   Operator         of Stack         Operation
                         30

   DUP              30   30          Duplicates     it    so we can      test    it
                                     twice.

   0<               30    0          Is it negative?        No (zero).

    SWAP             0   30          Swaps the flag       with the number.

    10 MOD 0=        0    1          Is it evenly      divisible   by 10?       Yes
                                     (one).

    +                     1          Adds the flags.


Adds the flags?      What happens     when you add flags?          Here are four
possibilities:
98                                                                          Starting      FORTH




  firstfla9

    flag
second


         result

Lo and behold,          the result   flag   is true  if either     or both
conditions       are true.  In this example,    the result  is one, which
means     "true."     If the input    number had been -30, then        both
conditions      would have been true and the sum would have been two.
Two is, of course, non-zero.       So as far as (g:] is concerned,    two is
as true as one.

Our simple-minded            definition,      then,    would be:

          VEGETABLE DUP 0< SWAP 10 MOD 0=                          +
            IF • II ARTICHOKE II THEN

Here's     an improved        version      of a previous        example     called     ?DAY.
The old ?DAY only caught entries     over thirty - one.                          But negative
numbers shouldn't be allowed either.     How about this:
          ?DAY       DUP 1 < SWAP 31 > +
             IF     IINO WAY II ELSE . " THANK YOU II THEN ;

The above two examples will always work because any "true" flags
will always be exactly   "l."   In some cases, however,  a flag may
be any non-zero  value, not just "l," in which case it's dangerous
to add them with [B. For example,

         1 -1 + • 0 ok

gives us a mathematically                  correct     answer     but     not   the    answer   we
want if 1 and -1 are flags.

For this reason,      FORTH supplies     a word called   [QB],which will
return    the correct   flag even in the case of 1 and -1.         An "or
decision"     is the computer    term for the kind of flag combination
we've been discussing.        For example,   if either the front door or
the back door is open (or both), flies will come in.                   -

Another      kind        of decision       is called       an   "and"      decision.        In an
4 DECISIONS, DECISIONS, •••                                                   99




"and" decision,    both conditions    must be true for the result to be
true.   For example, the front door and the back door must both be
open for a breeze to come throug~If           there are three or more
conditions,   they must all be true.f
How can we do this in FORTH? By using the handy word IAN~I·
Here's what IANDIwould do with the four possible combinations of
flags we saw earlier:




           ~                       ~               ~                   ~
JANI?)~ [ANDI~ IANDJµJ
                     ~ND\µ}



In other
           ~
            words,       only
                                   r» {lb {]Jr
                                the combination   "l l AND" produces   a result
of one.
Let's say we're looking for a cardboard             box that's   big enough   to
fit a disk drive which measures:

       height   6   11




       width 19"
       length   22"


The height,  width, and length requirements   all must be satisfied
for the box to be big enough.   If we have the dimensions of a box
on the stack, then we can define:

tFor   the Curious Newcomer
The use of words like "or" and "and" to structure                   part of an
application     is called    "logic."      A form of notation      for logical
statements     was developed      in the nineteenth        century   by George
Boole;     it is now called      Boolean      algebra.      Thus the term "a
Boolean flag" (or even just "a Boolean")              simply refers to a flag
that will be used in a logical        statement.
100                                                   Starting   FORTH




       BOXTEST ( length width height -
         6 > ROT 22 > ROT 19 > AND AND
         IF • II BIG ENOUGHII THEN ;
Notice that we've put a comment inside the definition, to remind
us of stack effects.   This is particularly  wise when the stack
order is potentially confusing or hard to remember.
You can test     BOXTESTwith the phrase:
      23 20 7 BOXTEST BIG ENOUGHok
As your applications    become . more sophist i cated, you will be able
to write statements    in FORTH that look like postfix      English and
are very easy to read.      Just define the individual     words within
the definition    to check some condition     somewhere, then leave a
flag on the stack.
An example     is:
       SNAPSHOT ?LIGHT ?FILM AND IF PHOTOGRAPH
                                             THEN ;
which checks that there is available    light and that there is film
in the camera before taking the picture.       Another example, which
might be used in a computer-dating   application,    is:
       MATCH HUMOROUSENSITIVE AND
         ART.LOVINGMUSIC.LOVINGOR AND SMOKINGNOT AND
         IF • 11 I HAVE SOMEONEYOU SHOULDMEET II THEN ;
where words like HUMOROUSand SENSITIVE have been defined       to
check a record in a disk file that contains information on other
applicants of the appropriate sex.
4 DECISIONS, DECISIONS, •••                                                    101



                                                         (\UEStion-dupe
Two Words with Built-in        [rF]s



The word !?DUP! duplicates             the top stack        value    only if it is
non-zero.      This can eliminate        a few surplus      words.    For example,
the definition

      : /CHECK     DUP IF / ELSE DROP THEN

can be shortened      to:

      : /CHECK     ?DUP IF / THEN



!ABORT"!
It may happen that somewhere in
a complex      application   an error
might occur (such as division       by
zero)    way down in one of the
low-level       words.     When this
happens    you don't just want the
computer     to keep on going,    and
you also don't want it to leave
anything    on the stack.

If you think such an error might
occur,     you can use the word
IABORT"J. IABORT"I expects        a flag
on the stack:         a "true"     flag
tells   it to "abort,"       which     in
turn clears     the stack and returns
execution         to the   terminal,
waiting      for someone       to type
something.       IABORT"! also prints
the name of the last interpreted
word,     as well       as whatever
message you want. t

Let's  illustrate.  We hope you're             not   sick    of /CHECK by now,
because here is yet another version:

      : /CHECK     DUP 0=    ABORT" ZERO DENOMINATOR" / ;


tFORTH-79 Standard

The Standard      includes the word !ABORT!, which differs            from !ABORT"!
only in that     it does not issue an error message.
102                                                                           Starting         FORTH




In this     version,  if the denominator  is zero,  any                             numbers       that
happen     to be on the stack will be dropped   and the                             terminal       will
show:

         8 0 /CHECK /CHECK ZERO DENOMINATOR

Just    as an       experiment,        try       putting        /CHECK       inside        another
definition:

         : ENVELOPE          /CHECK    • II THE ANSWER IS          II    •



and try

         8 4 ENVELOPE THE ANSWER IS 2 ok
         8 0 ENVELOPE ENVELOPE ZERO DENOMINATOR

The point      is that when /CHECK aborts,                  the rest of ENVELOPE is
skipped.       Also notice that the name                   ENVELOPE, not /CHECK, is
printed.

A useful word to use in conjunction   with !ABORT"! is !?STACK!, which
checks for stack underflow   and returns   a true flag if it finds it.
Thus the phrase:

         ?STACK ABORT" STACK EMPTY "

aborts     if the    stack    has underflowed.

FORTH uses      the     identical      phrase,       in fact.       But it waits          until      all
of    our definitions         have    Stopped       executing      before      it     performs      the
 ?STACK test,   because   checking    continuously                      throughout    execution
would needlessl      slow down the computer.t                           You're free to insert
a !?STACK! ABORT" phrase           at any critical                        or not-yet-tested
portion of your application.




t For Computer Philosophers
FORTH provides       certain    error checking    automatically.     But because
the FORTH operating             system    is so easy to modify,        users   can
readily    control      the amount of error      checking      their system will
do.    This flexibility      lets users make their own tradeoffs          between
convenience      and execution       speed.
4 DECISIONS, DECISIONS, •••                                                             103




                         words we've covered in this . chapter:
Here's a list of the FORTH


 IF XXX               IP:        (f --        )   If f is true (non-zero) exe-
      ELSE yyy                                    cutes xxx; otherwise executes
      THENzzz                                     yyy; continues      with zzz
                                                  regardless.   The phrase ELSE
                                                  yyy is optional.
                      (nl n2 -- f)                Returns true if nl and n2 are
                                                  equal.
                      (nl n2 -- n-diff)           Returns    true     (i.e.,            the
                                                  non-zero   difference)              if nl
                                                  and n2 are not equal.
 <                    (nl n2 -           f)       Returns  true         if nl    is less
                                                  than n2.
 >                    (nl n2 -           f)       Returns true if nl is greater
                                                  than n2.
 O=                   (n --       f)              Returns    true if         n is zero
                                                  (i.e.,  reverses           the truth
                                                  value).
 0<                   (n --       f)              Returns      true     if n is nega-
                                                  tive.
 O>                   (n --       £)              Returns    true     if n is positive.

 NOT                  (f --      f)               Reverses      the     result   of the
                                                  previous     test;     equivalent   to
                                                  O=.

 AND                  (nl n2 -           and)     Returns the logical           AND.
 OR                   (nl n2 -           or)      Returns the logical           OR.
 ?DUP                 (n -- n n) or               Duplicates        only if n is non-
                      (0 --      0)               zero.
 ABORT"XXX       II   (f --        )              If the flag is true, types out
                                                  the last word interpreted,
                                                  followed by the text.      Also
                                                  clears the user's stacks and
                                                  returns    control    to the
                                                  terminal.   If false, takes no
                                                  action.
 ? STACK              (     --   f)               Returns   true   if a stack
                                                  underflow    condition    has
                                                  occurred.
104                                                    Starting    FORTH




Review of Terms

Abort             as a general   computer term, to abruptly cease
                  execution    if a condition   occurs which the
                  program is not designed to handle, in order to
                  avoid producing    nonsense   or possibly doing
                  damage.
"And" decision    two conditions  that are combined such that            if
                  both of them are true, the result is true.
Branching         breaking the normally straightforward        flow of
                  execution,  depending    on conditions    in effect
                  at the time of exection.    Branching allows the
                  computer to respond differently        to different
                  conditions.
Comparison
operator          in general,   a command that compares one value
                  with another     (for example, determines   whether
                  one is greater     than the other) and sets a flag
                  accordingly,    which normally will be checked by
                  a conditional          operator.      In FORTH, a
                  comparison     operator     leaves the flag on the
                  stack.
Conditional
operator          a word, such as ll]:], which routes the flow of
                  execution    differently    depending  on some
                  condition (true or false).
Flag              as a general  computer term, a value stored in
                  memory which serves as a signal as to whether
                  some known condition    is true or false.  Once
                  the "flag is set," any number of routines     in
                  various parts of a program may check (or reset)
                  the flag, as necessary.
Logic             in computer        terminology,        the system    of
                  representing    conditions     in the form of "logical
                  variables,"    which can be either true or false,
                  and combining          these  variables    using such
                  "logical    operators"     as "and," "or," and "not,"
                  to form statements which may be true or false.
Nesting           placing  a branching     structure   within     an outer
                  branching structure.
"Or" decision     two conditions  that are combined such that            if
                  either of them is true, the result is true.
4 DECISIONS, DECISIONS, •••                                                               105




Problems -         Chapter 4
(answers     in the back of the book)


1.   What will        the phrase
             O= NOT

     leave        on the stack      when the argument            is
             l?
             0?
             200?

2.   Explain        what an artichoke             has to do with any of this.

3.   Define a word called CARD which,                        given a person's age on the
     stack, prints out either  of these                      two messages (depending  on
     the relevant  laws in your area):

             ALCOHOLICBEVERAGES PERMITTED                             or
             UNDERAGE

4.   Define a word called   SIGN.TEST that will test                           a number    on
     the stack and print out one of three messages:

             POSITIVE              or
             ZERO     or
             NEGATIVE

5.   In Chap. 1, we defined   a word called                           STARS in such a way
     that it always prints at least one star,                         even if you say
             0 STARS~
     Using the word STARS, define                          a new version     of STARS that
     corrects this problem.

6.   Write        the definition         for a word called            WITHIN which   expects
     three        arguments:
             (n low-limit        hi-limit        --

     and leaves         a "true"        flag    only      if "n" is within   the range
             low -l imit     <     n     <     hi-limit
106                                                               Starting   FORTH




7.    Here's a number-guessing       game (which you may enjoy writing
      more than anyone will enjoy playing).           First    you secretly
      enter   a number onto the stack       (you can hide your number
      after  entering     it by executing  the word PAGE, which clears
      the terminal    screen).   Then you ask another    player to enter a
      guess followed by the word GUESS, as in
           100 GUESS

      The computer will either   respond    "TOO HIGH," "TOO LOW," or
      "CORRECT!" Write the definition      of GUESS, making sure that
      the answer-number    will stay on the stack through    repeated
      guessing until the correct    answer is guessed, after which the
      stack should be clear.

8.    Using nested tests and [IT]... !ELSEj... !THEN! statements, write a
      definition  called   SPELLER which will spell out a number that
      it finds on the stack, from -4 to 4. If the number is outside
      this range,   it will print  the message     "OUT OF RANGE." For
      example:
           2 SPELLER TWO ok
           -4 SPELLER NEGATIVE FOUR ok
           7 SPELLER OUT OF RANGE ok

      Make it as short      as possible.   (Hint: the FORTH word !ABS!
      gives the absolute     value of a number on the stack.)
9.    Using your definition      of WITHIN from Prob. 5, write another
      number-guessing     game, called TRAP, in which you first enter a
      secret   value, then a second player    tries to home in on it by
      trapping    it between two numbers, as in this dialogue:

           0 1000 TRAP BETWEEN ok
           330 660 TRAP BETWEEN ok
           440 550 TRAP NOT BETWEEN ok
           330 440 TRAP BETWEEN ok

      and so on, until     the player   guesses   the   answer:
           391 391 TRAP YOU GOT IT! ok

      Hint:   you may have to modify the arguments  to WITHIN so
      that TRAP does not say "BETWEEN" when only one argument is
      equal to the hidden value.
                    5    THE PHILOSOPHY OF FIXED POINT


In this chapter    we'll introduce   a new batch   of arithmetic
operators.   Along the way we'll tackle the problem of handling
decimal points using only whole-number arithmetic.


Quickie   Operators

Let's statt with the real easy stuff.   You should have no trouble
figuring out what the words in the following table do.t
                                                                          pronounced:
------------------------------,
  l+                    (n --   n+l)          Adds one.
  1-                    (n      n-1)          Subtracts      one.
  2+                    (n      n+2)          Adds two.
  2-                    (n      n-2)          Subtracts      two.
  2*                    (n      n*2)          Multiplies       by two
                                              (arithmetic        left
                                              shift).
  2/                    (n -- n/2)            Divides     by two
                                              (arithmetic   right
.________________                             s_h_if_t_l
                                                     -----           ,~


The reason they have been defined as words in your FORTH system
is that they are used very frequently in most applications  and
even in the FORTH system itself.



tFor Beginners
We'll explain    what "arithmetic      left   shift"   is later     on.


                                       107
108                                                                     Starting   FORTH




There are three reasons         to use a word such as [±], instead       of one
and [TI, in your new definitions.                 First,  you save   a little
dictionary     space each time.       Second, since such words have been
specially     defined    in the "machine      language"    of each individual
type      of computer       to take     advantage        of the   computer's
architecture,       they execute   faster   than one and (B. Finally,         you
save a little      time during compilation.



Miscellaneous      Math Operators

Here's     a table   of four miscellaneous
math operators.          Like the quickie
operators,      these functions    should be
obvious from their names.



                                                            AuntMinandUncleMa><

  ABS                  (n --   l'nl)                  Returns   the absolute

  NEGATE               (n -    -n)                    Changes    the sign.

  MIN                  (nl n2 -- n-min)               Returns   the minimum.
  MAX                  (nl n2 -        n-max)         Returns   the maximum.


Here are two simple       word problems,          using jABsjand jMINj,            ~

Write a definition         which computes             the   difference       between   two
numbers,  regardless          of the order             in   which     the    numbers   are
entered.

        : DIFFERENCE      - ABS ;
This gives      the same result        whether    we enter
        52 37 DIFFERENCE 15 ok                   or
        37 52 DIFFERENCE . 15 ok
5 THEPHILOSOPHY
              OF FIXEDPOINT                                                     109




Write a definition    which computes the commission   that furniture
salespeople   will receive  if they've  been promised $50 or 1/10 of
the sale price, whichever   is less, on each sale they make.

         COMMISSION         10 /     50 MIN ;

Three    different      values     would produce   these   results:

        600 COMMISSION • 50 ok
        450 COMMISSION • 45 ok
        50 COMMISSION • 5 ok



The Return      Stack


We mentioned   before that there were still some stack                manipulation
operators  we hadn't discussed  yet. Now it's time.

Up till now we've been talking    about "the stack" as if there were
only one.   But in fact there are two: the "parameter      stack" and
the "return  stack."   The parameter    stack is used more often by
FORTH programmers,   so it's simply called   "the stack" unless there
is cause for doubt.

As you've     seen,     the parameter    stack   holds   parameters  (or
"arguments")    that are being passed from word to word. The return
stack, however,      holds any number of "pointers"      which the FORTH
system uses to make its merry way through the maze of words that
are executing     other words.   We'll elaborate   later on.

You the user can employ the return    stack as a kind of "extra
hand" to hold values temporarily while you perform operations  on
the parameter stack.




  PARA-                              RETURN
 MtTER                               STI\CK
 STACK
110                                                      Starting       FORTH




The return stack is a last-in       first - out structure,   just like the
parameter     stack, so it can hold many values.           But here's   the
catch:    whatever      you put on the return stack you must remove
again    before     you get to the end of the definition              (the
semicolon),    because at that point the FORTH system will expect to
find a pointer      there.   You cannot use the return stack to pass
parameters from one word to another.
The following  table lists the words associated          with the return
stack.   Remember, the stack notation   refers         to the parameter
stack.
  >R                (n -      )           Takes a value off
                                          the     parameter
                                          stack and pushes
                                          it onto the return
                                          stack .
  R>                    --   n)           Takes a value off
                                          the return     stack
                                          and pushes it onto
                                          the    parameter
                                          stack.
  I                     -    n)           Copies the .!.2E_ of      I
                                          the return    stack
                                          without affecting
                                          it.
  I'                (   -    n)           Copies the second
                                          item of the return
                                          stack without af-
                                          fecting it.
  J                     -    n)           Copies the third
                                          item of the return
                                          stack without af-
                                          fecting it.
5 THEPHILOSOPHY
              OF FIXEDPOINT                                                                       111




Thewords[Bl and~ transfera valueto andfromthe return
stack,     respectively.                 In the     cartoon     above,      where       the     stack
effect     was:

         (2 3 1 -    3 2 1)

This is the phrase            that       did it:

         >R SWAP R>

Each~      and its corresponding~        must be used together   in the
same definition   or, if executed interactively,   in the same line of
input (before you hit the RETURN key).


The other three words--[!], Ir], and ~--only £.2ll values                                 from the
return stack without removing them. Thus the phrase:
         >R SWAP I

would produce          the same result    as far              as it goes, but unless you
clean up your         trash t before   the next               semicolon   (or return key),
you will crash        the system.


To see      how ~,    ~,   and [!] might be used,                        imagine        you are     so
unlucky     as to need to solve the equation:

              ax 2 +bx+          c

with all     four values         on the stack         in the following         order:

              (a b   C X   -t-       )

(remember to factor              out first).




tYou might call        such an error               in your program       a "litter      bug."
112                                                             Starting   FORTH




                       Parameter       Return
      0Eerator         Stack           Stack
                       a b C X
      >R               a b C           X

      SWAP ROT         C b   a         X

      I                C b   a X       X


      *                C b   ax        X

      +                c (ax + b)      X


      R> *             C x(ax+b)

      +                x(ax+b)+c

Go ahead      and try it.    Load the following   definition:
          QUADRATIC ( a b C X -- n)
            >R SWAP ROT I * + R> *         +
Now test     it:
      2 7 9 3 QUADRATIC48 ok
One more note (it's a little  off the subject, but this is the first
chance we've had to note it): you have now learned two different
words with the name CT](remember the EDITOR'S "insert"        word?).
The reason the same name can refer to two separate      definitions,
depending     on the context, is that the words are in different
voe abular ies.
We briefly     mentioned    earlier  that the EDITOR is a vocabulary.
You can get into the EDITOR vocabulary          automatically     by using
certain    EDITOR commands, such as [!]. Another vocabulary              is
called    FORTH, which contains        all the other predefined      words
we've    covered      so far.     You can get back into        the FORTH
vocabulary    by starting    to comwle a new definition     (that is, when
the interpreter     sees the word l:J).
We mention all this now simply to amaze and impress you.                     The
real discussion of vocabularies comes in a future chapter.
5 THE PHILOSOPHY
               OF FIXEDPOINT                                                           113




An Introduction        to Floating-Point       Arithmetic


There      are many controversies            surrounding        FORTH.     Certain
principles      which FORTH programmers            adhere    to religiously       are
considered       foolhardy    by the proponents           of more traditional
languages.      One such controversy         is the question      of "fixed-point
representation"       versus "floating-point       representation."

If you already     understand  these     terms, skip ahead to the next
section,  where we '11 express    our views on the controversy.         If
you're a beginner,    you may appreciate     the following explanation.

First, what does floating  point mean?    Take a pocket                     calculator,
for example.  Here's what the display  looks like after                     each entry:


             You enter:                    Display     reads:
             1       5 0    X                          1.5

             2       2 3                              2.23

                                                     3.345


The decimal point "floats"            across the display          as necessary.        This
is called  a "floating point          display."
"Floating        point     representation"     is a way to store    numbers              in
computer         memory using          a form of scientific   notation.                  In
scientific       notation,     twelve million   is written:

      12 X 106

since    ten to the sixth     power equals    one million.     In many
computers twelve million     could be stored as two numbers:      12 and
6, where    it is understood     that 6 is the power of ten to be
multiplied   by 12, while 3.345 could be stored as 3345 and · -3.
The idea of floating-point        representation      is that the computer
can represent      an enormous      range    of numbers,    from atomic   to
astronomic,   with two relatively      small numbers.

What is fixed-point     representation?      It is simply the method of
storing  numbers in memory without storing        the positions  of each
number's decimal point.      For example, in working with dollars     and
cents,  all values   can be stored      in cents.   The program,  rather
than each individual      number, can remember the location        of the
decimal point.
For example,          let's   compare     fixed-point           and   floating-point
representations         of dollars - and-cents    values.
114                                                       Starting   FORTH




      Real-world           Fixed-point         Floating-point
          Value           Representation       Representation
         1.23                  123                   123(-2)
        10.98                 1098                  1098(-2)
       100.00                10000                      1(2)
        58.60                 5860                   586(-1)


As you can see, with fixed-point     all the values must conform to
the same "scale."    The decimal points must be properly      "aligned"
(in this case two places in from the right) even though they are
not actually  represented.    With fixed-point,    the computer treats
all the numbers as through they were integers.          If the program
needs to print    out an answer, however,       it simply inserts     the
decimal point two places in from the right before it sends the
number to the terminal or to the printer.


Why FORTH Programmers     Advocate    Fixed-Point

Many respectable   languages     and many distinguished     programmers
use floating-point    arithmetic      as a matter    of course.    Their
opinion   might be expressed      like this:   "Why should I have to
worry about moving decimal points around?         That's what computers
are for.  11




That's a valid question- - in fact it expresses the most significant
advantage    to floating-point   implementation.   For translating   a
mathematical   equation into program code, having a floating-point
language makes the programmer's life easier.                          •
The typical   FORTH programmer, however, perceives   the role of a
computer differently.     A FORTH programmer is most interested  in
maximizing the efficiency    of the machine.  That means he or she
wants to make the program run as fast as possible   and require as
little computer memory as possible.
To a FORTH programmer, if a problem is worth doing on a computer
at all, it is worth doing on a computer well.     The philosophy    is,
"If you just want a quick answer to a few calculations,     you might
as well use a hand-held        calculator."   You won't care i f the
calculator  takes half a second to display the result.      But if you
have invested      in a computer, you probably   have to repeat    the
same set of calculations           over and over and over again.
Fixed-point   arithmetic  will give you the speed you need.
Is the extra speed that noticeable?         Yes, it is. A floating - point
multiplication      or division    can take three times as long as its
equivalent     fixed-point     calculation.   The difference     is really
noticeable     in programs which have to do a lot of calculations
5 THE PHILOSOPHY
               OF FIXED POINT                                                           115




before sending  results  to a terminal   or taking some action.t
Most mini- and microcomputers   don't "think" in floating-point~
you pay a heavy penalty for making them act as though they do.
Here are some of the                reasons        you      might      prefer    to   have
floating-point capability.
        1.      You want to use your          computer        like     a calculator      on
                floating-point data.
        2.      You value the initial programming time more highly than
                the execution  time spent every time the calculation  is
                performed.
        3.      You want a number to be able to describe    a very large
                dynamic range (greater than -2 billion to +2 billion).
        4.      Your system includes a discrete    hardware floating-point
                multiply (a separate    "chip" whose only job is to perform
                floating-point  multiplication  at super high speeds).


tFor Experts

Many professional          FORTH programmers     who have been writing
complex       applications       for years     have    never   had to use
floating-point.        And their applications     often involve solutions
of differential       equations,   Fast Fourier Transforms,     non-linear
least        squares   fitting,   linear      regression,       etc.      Problems     that
traditionally  required  a main-frame    have been                       done on slower
minicomputers and microprocessors,    in some cases                      with an overall
increase in computation rate.
Most problems with physical         inputs and outputs, including weather
modeling,      image     reconstruction,            automated      electrical
measurements, and the like all involve input and output variables
that inherently       have a dynamic range of no more than a few
thousand to one, and thus fit comfortably               into a 16-bit integer
word. Intermediate       calculation      steps (such as summation) can be
handled     by the judicious        use of scaling        and double-length
integers    where required.       For example, one common calculation
step might involve multiplying         each data point by a parameter (or
by itself) and summing the result.           In fixed point, this would be a
16 x 16-bit multiply       and 32-bit summation.           In floating-point,
numbers are likely stored as 24-bit mantissa and 8-bit exponents.
The 24-bit multiply will take about 1.5 times longer and the 32-bit
addition 3-10 times longer than in fixed point.               There is also the
overhead of floating      all the input data and fixing all the output
data, approximately       equal to one floating-point           addition      each.
When these operat ~ons are performed               thousands    or millions       of
times,    the overall      saving     by remaining        in integer      form is
enormous.
116                                                                       Starting   FORTH




All of these are valid reasons.            Even Charles Moore, perhaps the
staunchest     advocate    of simplicity     in the programming community,
has occasionally         employed     floating-point     routines    when the
hardware     supported     it.  Other FORTH programmers          have written
floating-point      routines   for their mini- and microcomputers.          But
the mainstream       FORTH philosophy        remains:   "In most cases, you
don't need to pay for floating-point.                  11




FORTH backs its philosophy    by supplying   the programmer with a
unique set of high-level   commands called     "scaling  operators.                         11


We'll introduce  the first of these commands in the next section.
(The final   example in Chap. 12 illustrates     the use of scaling
techniques.)


Star-slash      the     Scalar

Here's     a math operator           that    is as useful   as it is unusual:        EZI-
  */                       (nl n2 n3 - -               Multiplies,      then    di-
                                n-result)              vides (nl*n2/n3).       Uses
                                                       a 32-bit    intermediate
                                                       result.


As its       name     implies,~             performs    multi-
plication,     then division.                 For example,
let's    say that the stack                 contains  these
three numbers:
         (225 32 100 --
~ will    first  multiply                   225 by 32, then
divide the result by 100.

This operator      is particularly               useful as an
integer-arithmetic         solution              to problems
such as percentage      calculations.

For example,        you could define           the word% like     this:
       : %     100 */ ;
so that      by entering          the number 225 and then the phrase:
       32 %
5 THEPHILOSOPHY
              OF FIXEDPOINT                                           117




you'd end up with 32% of 225 (that is, 72) on the stack. t

~ is not just      a ~ and a [21thrown together, though.        It uses a
"double - length    intermediate result." What does that        mean, you
ask?
Say you want to compute         34% of 2000.     Remember    that
single-precision     operators,  like ~ and [21, only work with
arguments and results within the range of -32768 to +32767. If you
were to enter the phrase:
     2000 34 * 100 /
you'd get an incorrect  result, because the "intermediate    result"
(in this case, the result of multiplication)       exceeds 32767, as
shown in the left column in this pictorial   simulation.
     2000 34 * 100 I              2000 34 100 */

     sin 3 le-le11!!th                          double-length
      ~                                     r
      110001                                         [,ooo)
      1       s4l                                              341
~fuoo@                               '*)I.....
                                           __ 6__s_o_o_o_!
    I tool                    l!ZJ                    I 1 ool
lZ) I9arba.,ef                        (/)
                                                        s•ol
But~      uses a double-length    intermediate   result,   so that its
range will be large       enough to hold the result        of any two
single-length  numbers multiplied together.    The phrase:
     2000 34 100 */
returns the correct answer because   the end result    falls   within the
range of single-length  numbers.

tFor the curious
The method of first multiplying two integers,
then dividing    by 100 is identical   to the
approach   most people take in solving    such
problems on paper.
118                                                                          Starting   FORTH




The previous          example        brings     up another       question:      how to round
off.

Let's    assume that         this    is the problem:

        If 32% o:f; the students   eating  at the school cafeteria  usually
        buy bananas,    how many bananas should be on hand for a crowd
        of 225? Naturally,      we are only interested   in whole bananas,
        so we'd like to round off any decimal remainder.


As our definition               now stands,          any value  to the right  of               the
decimal      is simply           dropped,           In other   words, the result                 is
"truncated."                                                                                      ·


        32% of:                                  Result:
                225 = 72.00                             72      exactly     con,ect
                226   72.32                             72      correct,     rounded down
                                                                (truncated)
                227 = 72.64                             72      truncated,      not rounded.


There is a way, however, with any decimal                            value of .5 or higher,
to round upwards to the next whole oanana.                             We could define   the
word R%, for "rounded percent," like this:
        : R%      10 */      5 + 10 / ;
so that        the phrase:
        227 32 R% •

will    give     you 73, which           is correctly      rounded   up.

Notice that we first divide by 10 rather  than 100. This gives                                   us
an extra decimal place to work with, to which we can add five:


                          Stack
        Operation         Contents
                          227       32    10

        */                               726
        5 +                              731

        10 /                              73
5 THEPHILOSOPHY
              OF FIXEDPOINT                                                                 119




The final          division  by ten sets           the value     to its     rightful    decimal
position.          Try it and see. t

A disadvantage    to this method of rounding   is that you lose one
decimal   place of range in the final result;   that is, it can only
go as high as 3,276 rather    than 32,767. But if that's   a problem,
you can always use double-length     numbers, which we'll introduce
later,  and still be able to round.



Some Perspective              on Scaling


Let's back up for a minute.                   Take the simple problem of computing
two-thirds of 171. Basically,                  there are two ways to go about it.

       1.     We could     compute   the value   of the fraction     2/3 by
              dividing    2 by 3 to obtain the repeating    decimal .666666,
              etc.     Then we could multiply    this value    by 171. The
              result would be 113.9999999, etc., which is not quite right
              but which could be rounded up to 114.
       2.     We could multiply   171 by 2 to get                    342.     Then     we could
              divide this by 3 to get 114.

Notice      that    the second           way is simpler    and more accurate.

Most computer languages     support the first way.                         "You can't have a
fraction  like two-thirds   hanging around inside                         a computer,"  it is
believed,   "you must express it as .666666, etc."

FORTH supports the second                   way.    ~ lets     you have       a fraction    like
two-thirds, as in:

       171 2 3 */
Now that we have a little                   perspective,     let's   take     a slightly    more
complicated example:




tFor     Experts

An even faster             definition:

         : R%       50 /     l+ 2/;
120                                                           Starting   FORTH




We want to distribute         $150 in proportion    to two values:t
        7,105     ?
        5,145     ?
       12,250    150
Again, we could solve         the problem this way:
        (7,105 / 12,250) X 150
and
        (5,145 / 12,250) X 150
but ror greater        accuracy;   we should say:
        (7,105 X 150) / 12,250
and
        (5,145 X 150) / 12,250
which in FORTH is written:
        7105 150 12250 */ . 87 ok
then
        5145 150 12250 */ . 63 ok


                              It can be said that
                              the values 87 and 63
                              are "scaled"     to 7105
                              and 5145. Calculating
                              percentages,       as we
                              did earlier,   is also a
                              form of scalin~Fot
                              this   reason,    ~ is
                              called     a "scaling
                              operator."




tFor Beginners        Who Like Word-problems
Here's    a word-problem       for the above example:
The boss says he'll      divide     a $150 bonus between       the two
top-selling  marketing representatives    according   to their monthly
commissions.     When the receipts       are counted,     the top two
commissions   are $7,105 and $5,145. How much of the bonus does
each marketing rep get?
5 THE PHILOSOPHY
               OF FIXEDPOINT                                                121




Another scaling    operator    in FORTHis l*/MODI:


  */MOD               (ul u2 u3 --          MJJltiplies, then
                         u-rem u-result)    divides (ul*u2/u3).
                                            Returns     the re-
                                            mainder     and the
                                            quotient.     Uses a    ~
                                            double-length     in-     '
                                            termediate result.         ~
~-----'                                                             ,. .
We'll let you dream up a good example for ~ yourself.


Using Rational     Approximationst

So far we've only used scaling    operations  to work on rational
numbers.   They can also be used on rational    approximations    of
irrational  constants, such as pi or the square root of two. For
example, the real value of pi is
     3.14159265358, etc.
but to stay within the bounds          of single-length     arithmetic,      we
could write the phrase:
     31416 10000 */
and get a pretty      good approximation.
Now we can write       a definition    to compute the area     of a circle,
given its radius.      We'll translate   the formula:


into FORTH. The value of the radius will be on the stack,                  so we
IDUPIit and multiply it by itself, then star-slash the result:



t For Math-block    Victims:
You can skip this section if it starts making your brain itch. But
if you're feeling particularly   smart today, we want you to know
that •••
A rational  number is a whole number or a fraction          in which the
numerator and denominator are both whole numbers. Seventeen is
a rational number, as is 2/3. Even 1.02 is rational,         because it's
the same as 102/100. -l 'l:, on the other hand, is irrational.
122                                                                                  Starting      FORTH




       : PI        DUP * 31416 10000 */               :
Try it with         a circle      whose radius            is ten      inches:
       10     PI       314 ok

But for even more accuracy,     we might wonder if there is a pair                                          of
integers    besides 31416 and 10000 that is a closer approximation                                          to
pi.   Surprisingly,  there is. The fraction:

       355 113 */

is accurate   to more than six                        places   beyond              the   decimal,           as
opposed to less than four places                       with 31416.

Our new and improved                 definition,          then,     is:

       : PI        DUP * 355 113 */ :

It turns out that you can approximate      nearly   any constant   by
many different  pairs of 2g1tegers, all numbers less than 32768, with
an error of less than 10 • t




tFor   Really        Dedicated        Mathephiles

Here's     a handy           table        of rational             approximations           to   various
constants:

                       Number                                        Aeeroximation        ~
                                     1[  = 3 .1 41                    355 / 113           8.5 X     10·~
                                    y2 = 1.414                      19601 / 13860         1.5 X     1 o·•
                                    ft=    1. 73 2                  18817 / 10864         1.1 X     1 o·•
                                       e = 2.718                    28667 /1 0546         5.5 X     1 o·•
                                   y10 = 3.162                      22936 / 7253          5. 7 X    1 o·•
                                   W = 1.059                        26797 / 25293         1.0 X     1 o·•
                   1og 10 2 / 1. 6 3 8 4   0 . 183                   2040 / 11103         1.i X     10 ..
                        l n2 / 16.384 = 0.042                         485 / 11464         1.0 X     10·1
           . 001° / 22-bi t rev               0.858                 18118 / 21109         1.4 X     1 o·•
        arc-sec / 22-bit    rev               0.309                  9118 / 29509         1.0 X     10·9
                                     C    :   2.9979248             24559 / 8192          1. 6 X    10-s
5 THEPHILOSOPHY
              OF FIXEDPOINT                                                 123




Here's a list   of the FORTHwords we've covered         in this chapter:


  l+                (n --    n+l)        Adds one.
  1-                (n --    n-1)        Subtracts     one.
  2+                (n -- n+2)           Adds two.
  2-                (n -- n-2)           Subtracts     two.
  2*                (n -- n*2)           Multiplies     by two (arithmetic
                                         left shift)
  2/                (n -     n/2)        Divides    by two (arithmetic
                                         right shift)
  ABS               (n - !nil            Returns the absolute      value.
  NEGATE            (n --    -n)         Changes the sign.
  MIN               (nl n2 -- n-min)     Returns the minimum.
  MAX               (nl n2 -- n-max)     Returns the maximum.
  >R                (n --     )          Takes    a value     off the
                                         parameter stack and pushes it
                                         onto the return stack.
  R>                (   --   n)          Takes a value off the return
                                         stack and pushes it onto the
                                         parameter stack.
  I                     -    n)          Copies the ~ of the return
                                         stack without affecting it.
  I'                    - - n)           Copies the second         item of
                                         the return     stack      without
                                         affecting  it.
  J                 (   -    n)          Copies      the third item of the
                                         return        stack  without  af-
                                         fecting      it.
  */                (nl n2 n3 -          Multiplies,   then divides (ul*
                       n-result)         n2/n3). Uses a 32-bit interme-
                                         diate result.
  */MOD             (ul u2 u3 --         Multiplies,     then divides (ul*
                       u-rem u-result)   u2/u3).     Returns the remain-
                                         der and the quotient.        Uses a
                                         double-length       intermediate
                                         result.
124                                                         Starting   FORTH




Review of Terms

Double-length
intermediate
result                a double-length        value    which    is created
                      temporarily   by a two-part operator,      such as~,
                      so that the "intermediate      result" (the result of
                      the first operation)     is allowed to exceed the
                      range of a single-length        number, even though
                      the initial   arguments and the final result are
                      not.
Fixed-point
arithmetic            arithmetic    which deals with numbers which do
                      not themselves      indicate      the location  of their
                      decimal    points.       Instead,     for any group of
                      numbers, the program assumes the location              of
                      the decimal        point     or keeps      the decimal
                      location    for all such numbers as a separate
                      number.
Floating-point
arithmetic            arithmetic    which deals with numbers which
                      themselves    indicate    the location   of their
                      decimal points.      The program must be able to
                      interpret   the true value of each individual
                      number before any arithmetic    can be performed.
Parameter     Stack   in FORTH, the region of memory which serves as
                      common ground between various operations         to
                      pass arguments     (numbers, flags, or whatever)
                      from one operation    to another.
Return stack          in FORTH, a region of memory distinct  from the
                      parameter stack which the FORTH system uses to
                      hold "return   addresses" (to be discussed   in
                      Chap. 9), among other things.     The user may
                      keep values on the return stack temporarily,
                      under certain conditions.
Scaling               the process     of multiplying      (or dividing)    a
                      number by a ratio.     Also refers to the process
                      of multiplying     (or dividing)      a number by a
                      power of ten so that all values in a set of
                      data may be represented        as integers   with the
                      decimal point assumed to be in the same place
                      for all values.
5 THEPHILOSOPHY
              OF FIXEDPOINT                                                             125




Problems -         Chapter     5


1.   Translate          the following        algebraic      expression      into   a FORTH
     definition:

                ---ab
                    C


     given       {a b c --     )
2.   Given these four numbers on the stack:
           (6 70 123 45 --         )

     write an expression               that prints   the largest     value.

Practice        in Scaling

3.   In "calculator  style,"               convert       the following      temperatures,
     using these formulas:

                 = OF - 32
                        1.8
           Op    = (OC x 1.8) + 32
           °K    = 0 c + 273
     {For now, express             all arguments and results        in whole
     degrees.)
     aj     o° Fin  Centigrade
     b)     212° F in Centigrade
     c)     -32° F in Centigrade
     d)     16° C in Fahrenheit
     e)     233° K in Centigrade
4.   Now define words to perform the conversions                         in Prob. 3.
     Use the following names:
           F>C      F>K       C>F      C>K    K>F        K>C
     Test them with the above values.
                           6    THROWIT FOR A LOOP


In Chap.       4 we learned     to program      the computer      to make
"decisions"       by branching    to different    parts   of a definition
depending        on the outcome      of certain    tests.    Conditional
branching      is one of the things that make computers as useful as
they are.
In this chapter,     we'll see how to write definitions              in which
execution    can conditionally     branch back to an earlier            part of
the same definition,      so that some segment will repeat          again and
again.    This type of control     structure     is called    a "loop."      The
ability   to perform loops is probably        the most significant        thing
that makes computers as powerful as they are.              If we can program
the computer to make out one payroll         check, we can program it to
make out a thousand of them.
For now we'll wri~e loops               that do simple things    like printing
numbers at your terminal.               In later chapters,  we'll learn to do
much more with them.


Definite      Loops --   [Doj... (EooPJ

One type of loop structure   is called a "definite   loop."   You, the
programmer,  specify   the number of times the loop will loop.       In
FORTH, you do this by specifying       a beginning     number and an
ending number (in reverse    order) before the word [QQ]. Then you
~ the words which you want to have repeated        between the words
l.QQjand ILOOPI. For example

      : TEST      10 0 bO CR • " HELLO " LOOP ;
will print a carriqge          return    and "HELLO" ten times,   because   zero
from ten is ten.




                                           127
128                                                                              Starting     FORTH




        TEST
        HELLO
        HELLO
        HELLO
        HELLO
        HELLO
        HELLO
        HELLO
        HELLO
        HELLO
        HELE'ook

Like     in    [fflr.JTHENl statement,             which also        involves    branching,    a
iDOl••. LOOP           statement   must           be contained            within    a {single)
Clefinition.

The ten        is called     the     "limit"     and the      zero   is called      the     "index."


         FORMULA:

                limit    index     DO ••• LOOPt


Here's        what happens         inside      a [QQ]
                                                   •••JLOOPl:




                                     §jf£TI.IR~
First    @Q]tputs the index
                            n        ~          STA<K



                                            and the   limit    on the    return      stack.
                                                                                                I
tFor     the    Timid Beginner

Go ahead!          Nobody's        looking.

         : TEST         1000 0 DO • 11 I'M GOING LOOPYI II LOOP ;

Go on, execute             it!   How often have            you been     able      to tell     anyone
to do something             a thousand   times?


!half-brother           of the     DODO bird.
6 THROW IT FOR A LOOP                                                      129




                                                            \ LOOPJ
Then execution  proceeds          to the   up till    the word [LOOPI.t
words inside the loop,




If the   index   is less   than   the      and adds    a one to the
limit, !1L@I reroutes      execution       index.
back to DO,


   LATER:

                 ~
                 fill
Eventually the index reaches   ten, and !LOOP!lets           execution    move
on to the next word in the definition.


+(who just emerged from its loophole)
130                                                         Starting      FORTH




Remember that the FORTH word [!] copies the top of the return
stack onto the parameter stack.  You can use [!] to get hold of the
current    value of the index each time around.       Consider  the
definition
       DECADE 10 0 DO I            LOOP
which executes     like this:
      DECADEO 1 2 3 4 5 6 7 8 9 ok
Of course, you could pick any range            of numbers (within      the range
of -32768 to +32767):
      : SAMPLE -243 -250 DO I .             LOOP
SAMPLE -250 -249 -248 -247 -246 -245 -244 ok
Notice that even negative    numbers increase            by one each       time.
The limit is always higher than the index.
You can leave a number on the stack to serve              as an argument      to
something inside a~   loop. For instance,
      : MULTIPLICATIONS CR 11 l DO DUP I * . LOOP DROP
will produce     the following   results:
      7 MULTIPLICATIONS
      7 14 21 28 35 42 49 56 63 70 ok
Here we're simply multiplying    the current value of the index by
seven each time around.     Notice that we have to IDUPIthe seven
inside the loop so that a copy will be available     each time and
that we have to IDROPIit after we come out of the loop.
A compound    interest    problem   gives    us the opportunity       to
demonstrate some trickier   stack manipulations   inside a~     loop.
Given a starting   balance, say $1000, and an interest  rate, say 6%,
let's write a definition   to compute and print a table like this:
      1000 6 COMPOUND
      YEAR1 BALANCE1060
      YEAR2 BALANCE1124
      YEAR3 BALANCE1191
                                        etc.
for twenty years.
First we'll load      R%, our previously-defined         word from Chap. 5,
then we'll define
6 THROWIT FOR A LOOP                                                     131




          COMPOUND ( amt int --
            SWAP 21 1 DO • 11 YEAR II I •          3 SPACES
             2DUP R% + DUP • " BALANCE"                CR LOOP 2DROP




                              &ALANC.E




                                          El
                                               INTEREST"
                               P.AT£
                                               !!AP.WED

             RUNNIN6                                           NEW
                              Bl'ILANCE        BALANCE
              B/ILIINCf                                       &ALANCE'

              1111Tr11esr
                               RATE             RAT<           RATE'
               P.ATr




Each time through           the loop, we do a l2DUPJ so that we always
maintain a running           balance and an unchanged interest    rate for
the next go-round.          When we're finally done, we l2DROP!them.


Getting     ITT')fy

The index can also serve as a condition   for an ~ statement.  In
this way you can make something special happen on certain passes
through the loop but not on others.  Here's a simple example:
          RECTANGLE 256 0 DO I 16 MOD0= IF
            CR THEN "*" LOOP
RECTANGLEwill print 256 stars, and at every sixteenth    star it
will also perform a carriage return at your terminal. The result
should look like this:
                            ****************
                            ****************
                            ****************
                            ****************
                            ****************
                            ****************
                            ****************
                            ****************
                            ****************
                            ****************
                            ****************
                            ****************
                            ****************
                            ****************
                            ****************
                            ****************
132                                                                                      Starting         FORTH




And here's   an example from                       the     world        of nursery        rhymes.          We'll
let you figure this one out.

         POEM CR 11 1 DO I • • 11 LITTLE 11
            I 3 MOD O= IF • 11 INDIANS II CR THEN LOOP
                 11
                    INDIAN BOYS. 11 1



Nested      Loops


In the last section    we defined    a word called      MULTIPLICATIONS,
which contained     a [Do]... jLOOPj. If we wanted      to, we could put
MULTIPLICATIONS inside another       @QJ
                                       ... jLOOP!, like this:
      : TABLE            CR 11 1 DO I          MULTIPLICATIONS LOOP 1

Now we'll          get   a multiplication            table       that     looks    like        this:

      1 2 3 4 5 6 7 8 9 10
      2 4 6 8 10 12 14 16 18 20
      3 6 9 12 15 18 21 24 27 30
                                                                 etc.
      10 20 30 40 50 60 70 80 90 100

because  the I!] in                the     outer         loop     supplies         the         argument      for
MULTIPLICATIONS.
You can also             nest     IQQ]loops        inside        one     another         all     in the     same
definition:

         TABLE CR 11 1 DO
           11 l DO I J * 5 U.R                       LOOP CR LOOP

Notice      this     phrase       in the     inner       loop:

      I J    *                                                                       [iJ inde,c
In Chap. 5 we mentioned         that    the word ~                                   [!!] limit
copies   the third   item of the return       stack
onto the parameter       stack.      It so happens                                   (1J inde><
that   in this   case the third        item on the
return stack is the index of the outer loop.                                                      limit
Thus the phrase   "I J *" multiplies                             the two
indexes to create   the values in the                            table.
Now what about             this    phrase?

      5 U.R
6 THROWIT FOR A LOOP                                                               133




This is nothing more than a fancy G]that is used to print numbers
in table    form so that    they  line up vertically.    The five
represents   the number of spaces we've decided each column in the
table should be. The output of the new table will look like this:


        1        2      3    4    5       6     7    8       9    10
        2        4      6    8   10      12     14   16   18      20
        3        6      9   12   15      18     2i   24   27      30    etc.

Each number takes five spaces,       no matter   how many digits        it
contains.    (rn:;:] stands for "unsigned      number-print,      right
justified."   The term "unsigned,"      you may recall,      means you
cannot use it for negative  numbers.)



!+LOOP!

If you want the index to go up by some number other than one
each time around, you can use the word !+LOOP! instead of !LOOP!.t
!+LOOP! expects  on the stack the number by which you want the
index to change.   For example, in the definition
        : PENTAJUMPS 50 0 DO I .                 5 +LOOP ;
the index            will go up by five       each time, with this     result:
        PENTAJUMPS 0 5 10 15 20 25 30 35 40 45 ok

while       in

        : FALLING           -10 0 DO I • -1 +LOOP ;

the index            will go down by one each time, with this            result:
        FALLING 0 -1 -2 -3 -4 -5 -6 - 7 -8 -9 -10 0k

The argument for !+LOOP!, which is called     the "increment,"                       can
come from anywhere,    but it must be put on the stack each                        time
around.  Consider this experimental  example:
        : INC-COUNT           DO I .     DUP +LOOP DROP ;




tFor    the Curious

A third~              loop ending      word is introduced        in Chap. 7.
134                                                             Starting      FORTH




There is no increment   inside the definition; instead,    it will have
to be on the stack when INC-COUNT is executed,         along with the
limit and index.   Watch this:

      Step   up by one:

         1 5 0 INC-COUNT 0 1 2 3 4 ok

      Step up by two:
         2 5 0 INC-COUNT 0 2 4 ok

      Step   down by three:
         -3 -10 10 INC-COUNT 10 7 4 1 -2 -5 -8 ok


Our next example   demonstrates        an increment      that     cha-nges       each
time through the loop.

      : DOUBLING 32767 1 DO I •         I +LOOP ;

Here the index itself  is used as the increment             {I +LOOP), so that
starting with one, the index doubles each time,            like this:
      DOUBLING
       1 2 4 8 16 32 64 128 256 512 1024 2048 4096 8192 16384 ok

(We chose     32767 as our limit    because   it   is our highest          allowable
number   in single   - l e ngth.)

Notice that in this example we don't ever want the argument for
l+LOOPl to be zero, because  if it were we'd never come out of the
loop.  We would have created   what is known as an "infinite loop."
6 THROWIT FOR A LOOP                                                                  135




li5ojing It -     FORTH style


There are a tew th!ngs to remember betore you go ott and write
some [QQIloops of your own.

First,    keep this    simple    guide     in mind:


                              Reasons      for Termination


  Execution      makes ij5 exit      from a loop when


                                                          I I
                                                          @m.
  going     up •••

                                                   .. )                               )
                                                                                      "



                ... the index     has reached         or passed      the limit.




  going     down •••      ~
                           ~--n~
                               .~ a
                        11111111111111//111/l~



                     .,. the index has passed             the   limit--not    when it has
                         me e l y reached it.
                          1

But a [QQI
         loop always            executes     at least      once:
         : TEST 100 10 DO I • -1 +LOOP ;
         TEST 10 ok

Second, remember          that the         words [Do] and !LOOP! are branching
commands and that         therefore         they can only be executed   inside            a
136                                                          Starting      FORTH




deftnition.       This means that you cannot        design/test         your   loop
definitions      in "calculator  style" unless      you simulate         the   loop
yourself;

Let's    see how a fledgling      FORTH programmer     might go about
design/testing    the definition   of COMPOUND(from the first section
of this chapter).     Before adding the ~ messages,     the programmer
might begin by jotting     down this version  on a piece of paper:

         COMPOUND ( amt :int -- )
           SWAP 21 1 DO I • 2DUP R% + DUP •           CR LOOP 2DROP ;

The programmer   might test this version         at the terminal,         using G]
or .s to check the result of each step.          The "conversation"          might
look like this:


              1000 6 SWAP . Smmm)
              6 1000 ok
first         2DUP • S---     --~        In simulation,     the programmer
time          6 1000 6 1000 ok           omits the "limit       index   DO"
thru                                     phrase,      as well      as any
                                         reference    to I.
              R % • SC!J!lim
              6 1000 60 ok

              + .srmmm                   In simulation,    the programmer
              61060 ok~                  can omit the     "DUP " phrase.

second        2DUP R% +    .SmI!lll3   ~---------             - -------'
time          6 1124 ok

              2DROP.S•;~                 Everything     seems to be work-
              EMPTY ok                   ing,     so the    programmer
                                         pretends     the last    loop has
                                         finished    and checks that the
                                         stack is clear.
6 THROWIT FOR A LOOP                                             137




                          A Handy Hint
                     How to Clear the Stack

Sometimes a beginner will unwittingly write a loop which leaves     a
whole lot of numbers on the stack.   For example

     : FIVES   100 0 DO I 5 . LOOP
instead   of
     : FIVES   100 0 DO I 5 * • LOOP

If you see this happen to anyone (surely it will never happen to
you!) and if you see the beginner typing in an endless succession
of dots to clear the stack, recommend typing in
     xx
XX is not a FORTHword, so the text interpreter    will execute    the
word IABORT"I,which among other things clears    both stacks.     The
beginner will be endlessly grateful.
138                                                                   Starting     FORTH




Indefinite       Loops


While oo:QJ  loops are called  definite   loops,  FORTH also supports
"indefinite"     loops. This type of loop will repeat       indefinitely
or until some event occurs.    A standard   form of indefinite      loop is

        BEGIN • • • UNTIL

The jBEGINj... jUNTILI loop         repeats    until    a condition   is "true."

The useage       is

        BEGIN xxx f UNTIL

where "xxx" stands     for the words that you want to be repeated,
and "f" stands   for a flag.     As long as the flag is zero (false),
the loop will    continue     to loop,  but when the flag   becomes
non-zero (true), the loop will end.




                                         (olwca~Srepe"-t.s
                                          11t lee1st orice)




An example of a definition                that uses a jBEGINj••. l!ffi.'!'.!.!d
                                                                            statement
is one we mentioned  earlier,              in our washing machine example:

          TILL-FULL        BEGIN      ?FULL UNTIL ;

which    we used       in the   higher-level      definition

          FILL        FAUCETS OPEN TILL - FULL FAUCETS CLOSE

?FULL will be defined       to electronically     check a switch     in the
washtub that indicates     when the water reaches       the correct   level.
It will return zero if the switch is not activated         and a one if it
is.    TILL-FULL does nothing      but repeatedly    make this test over
and over (thousands       of times per second)       until  the switch       is
finally    activated,  at which time execution      will come out of the
loop.     Then the u] in TILL-FULL will return the flow of execution
to the remaining      words in FILL, and the water faucets          will be
turned off.

Sometimes     a programmer    will delibera~ely   want to create                        an
infinite  loop.    In FORTH, the best way is with the form
6 THROWIT FOR A LOOP                                                          139




     BEGIN xxx O UNTIL

The zero supplies    a "false"      flag    to the word IUNTILI, so the loop
will repeat eternally.

Beginners usually want to avoid infinite             loops, because executing
one means that they lose control              of the computer      {in the sense
that only the words inside             the loop are being executed).           But
infinite       loops    do have their      uses.    For instance,       the text
interpreter       is part of an infinite     loop called     jQUITi, which waits
for input, interprets        it, executes    it, prints    "ok," then waits for
input once again.          In most microprocessor-controlled            machines,
the highest-level          definition     contains     an infinite     loop that
defines     the machine's    behavior.

Another   form of indefinite      loop     is used in this   format:
     BEGIN xxx f WHILE yyy REPEAT
Here the test occurs halfway through the loop rather    than at the
end. As long as the test is true, the flow of execution    continues
with the rest of the loop, then returns   to the beginning     again.
If the test is false, the loop ends.




Notice    that  the effect      of the test is opposite  that             in the
!BEGIN! •.• !UNTIL! construction.      Here the loop repeats               while
something is true {rather than until it's true).

The indefinite     loop structures     lend themselves       best to cases in
which you're waiting      for some external      event to happen, such as
the closing    of a switch or thermostat,      or the setting     of a flag by
another   part of an application         that is running      simultaneously.
So for now, instead        of giving     examples,    we just want you to
remember that the indefinite       loop structures    exist.
140                                                  Starting   FORTH




The Indefinitely      Definite   Loop

There is a way to write a definite  loop so that it stops short of
the prescribed limit if a truth condition  changes state, by using
the word LEAVE. !LEAVE!causes the loop to end on the very next
JLOOPJor +LOOP.




      Sometime during the course of the loop (while !LOOP[ is
      asleep   at the switch),   the word LEAVE sets the limit to
      equal the index.     Now the next time LOOP is executed, the
      loop will terminate.

watch how we rewrite      our earlier  definition  of COMPOUND.
Instead of just letting the loop run twenty times, let's get it to
quit after twenty times or as soon as our money has doubled,
whichever occurs first.
We'll simply add this phrase:
      2000 > IF LEAVE THEN
like this:
             DOUBLED 6 1000     21 1 DO CR
               ."YEAR"    I 2 U.R
               2DUP R¾ + DUP          BALANCE "
               DUP 2000 > IF" CR CR."   MORE THAN DOUBLED IN"
                               I . . " YEARS " LEAVE THEN
                                             LOOP 2DROP;

The result     will look like this:
6 THROWIT FOR A LOOP                                          141



   DOUBLED
   VEAR 1     BALANCE1060
   YEAR 2     BALANCE1124
   VEAR 3     BALANCE1191
   VEAR 4     BALANCE1262
   YEAR 5     BALANCE1338
   YEAR 6     BALANCE1418
   YEAR 7     BALANCE1503
   YEAR 8     BALANCE1593
   YEAR 9     BALANCE1689
   YEAR 10    BALANCE1790
   YEAR 11    BALANCE1897
   YEAR 12    BALANCE2011

    MORETHAN DOUBLEDIN 12 YEARS Ok

One of the problems at the end of this chapter asks you to rework
DOUBLED so that it expects     the parameters    of interest  and
s arting balance, and computes by itself the doubled balance that
 LEAVE will try to reach.
142                                                            Starting      FORTH




                  Two Handy Hints:         [PAGE]
                                                and [Qu"fT]


To give a neater    appearance   to your loop outputs   (such as tables
and geometric    shap~ou        might want to clear   the screen      first
by using the word ~-           You can execute   !PAGE! interactively
like this:

      PAGE RECTANGLE

which will clear the screen before printing     the rectangle that we
defined   earlier  in this chapter.    Or you could put !PAGE! at the
beginning   of the definition,  like this:
       RECTANGLE PAGE 256 0 DO
          I 16 MOD0= IF CR THEN , " *" LOOP

If you don't      want the "ok"       to    appear     upon    completion of
execution,     use the word ~-                Again,     you   can use ~
interactively:

      RECTANGLEQUIT

or you can make !QUIT! the last      word in the definition          (just   before
the semicolon).
6 THROWIT FOR A LOOP                                                       143




Here's   a list   of the FORTHwords we've covered       in the chapter:



  DO ••• LOOP        DO: (limit             SE!ts up a finite   loop,    given
                       index    )           the index range.
                     LOOP: ( -- )

  DO •.. +LOOP       DO: (limit             Like DO ••• LOOP except adds
                       index -- )           the value of n (instead   of
                     +LOOP: (n --           always one) to the index.

  LEAVE               (   --   )            Terminates  the loop        at the
                                            next LOOP or +LOOP.

  BEGIN •••          UNTIL: (f --       )   Sets up an indefinite    loop
    UNTIL                                   which ends when f is true.

  BEGIN XXX          WHILE: (f --       )   Sets up an indefinite    loop
    WHILE yyy                               which always executes      xxx
    REPEAT                                  and also executes yyy if f is
                                            true. Ends when f is false.

  U.R                 (u width --   )       Prints the unsigned    single-
                                             length   number,      right-
                                            justified  within   the field
                                            width.

  PAGE                (   --   )            ciears  the terminal   screen
                                            and resets    the terminal's
                                            cursor to the upper left-hand
                                            corner.

  QUIT                (   --   )            Terminates execution     for the
                                            current   task and returns
                                            control to the terminal.
144                                                      Starting   FORTH




Review     of Terms

Definite     loop     a loop structure   in which the words contained
                      within the loop repeat     a definite  number of
                      times.   In FORTH, this number depends on the
                      starting   and ending counts (index and limitj
                      which are placed     on the stack prior to the
                      execution of the word lliQ].
Infinite     loop     a loop structure in which the words contained
                      within the loop continue to repeat without any
                      chance of an external    event stopping     them,
                      except  for the shutting  down or resetting     of •
                      the computer.
Indefinite     loop   a loop structure   in which the words contained
                      within the loop continue     to repeat until some
                      truth condition   changes state (true-to-false     or
                      false-to - true). In FORTH, the indefinite     loops
                      begin with the word !BEGIN!.
6 THROWIT FOR A LOOP                                                                      145




Problems   -     Chapter      6


In Problems 1 through 6, you will create          several              words which       will
print  out patterns   of stars     (asterisks).     These              will involve       the
use of ill§] loops and !BEGIN! ... jUNTILI loops.



1.   First create a word named STARS which                      will   print   out n stars
     on the same line, given non the stack:

       10 STARS Gi1!m)            **********      ok
2.   Next define BOX which prints out a rectangle                         of stars,     given
     the width and height (number of lines),  using                      the stack      order
     (width height -- ) .

           10 3 BOX
           **********
           **********
           **********             ok
3.   Now create   a word named \STARS which will print       a skewed
     array of stars  (a rhomboid),   given the height   on the stack.
     Use a [QQ]loop and, for simplicity,   make the width a constant
     ten stars.

           3 \STARS
               **********
                **********
                 **********            ok
4.   Now create  a word which slants   the stars the other direction;
     call it /STARS.    It should take the height     as a stack input
     and use a constant   ten width.  Use a [QQ]loop.

5.   Now redefine          this    last     word, using   a !BEGIN! ••• jUNTILJ loop.
146                                                            Starting   FORTH




6,    Write   a definition  called      DIAMONDS which will print out the
      given   number of diamonds      shapes, as shown in this example:

      2 DIAMONDS       *
                      ***
                     *****
                    *******
                   *********
                  ***********
                 *************
                ***************
               *****************
              *******************
              *******************
               *****************
                ***************
                 *************
                  ***********
                   *********
                    *******
                     *****
                      ***
                         *
                         *
                        ***
                     *****
                    *******
                   *********
                  ***********
                 *************
                ***************
               *****************
              *******************
              *******************
               *****************
                ***************
                 *************
                  ***********
                   *********
                    *******
                     *****
                      ***
                          *
7.    In our discussion         of !LEAVE! we gave         an example       which
      computed 6% compound interest         on a starting      balance    of $1000
      for 20 years     or until    the balance      had doubled,       whichever
      came first.     Rewrite this definition        so that it will expect       a
      starting    balance    and interest      rate    on the stack     and will
      !LEAVE! when this starting      balance     has doubled.
6 THROWIT FOR A LOOP                                                        147




8.   Define     a word called    ** that     will   compute   exponential
     values,   like this:

          7 2 ** . 49 ok
          (seven squared)

           2 4 ** . 16 ok
           (two to the fourth   power)

     For simplicity,  assume positive      exponents    only (but make sure
     ** works correctly     when the       exponent    is one--the   result
     should be the number itself).
                  7 A NUMBER
                           OF KINDSOF NUMBERS

So far we've only talked about signed single-length numbers.    In
this chapter we'll introduce unsigned numbers and double-length
numbers, as well as a whole passel of new operators to go along
with them.
The chapter   is divided   into   two sections:
     For beginners--this  section explains   how a computer looks at
     numbers and exactly     what is meant by the terms signed or
     unsigned anq by single-length   or double-length.

     For everyone--this      section continues     our discussion   of FORTH
     for beginners      and experts    alike,   and explains      how FORTH
     handles   signed     and unsigned,     single-    and double-length
     numbers.




                                     149
150                                                                                                    Starting          FORTH




                                    SECTION I -                    FOR BEGINNERS



Signed     vs. Unsigned                   Numbers
                                                                                             0000 000000000100

All digital      computers   store numbers                             in



                                                                                                                              I
                                                                                             000000000010 1001
binary   form.t      In FORTH, the stack                               is
sixteen       bits    wide    (a "bit"     is                           a                    00000000 00000000
"binary     digit").     Below is a view                               of                I                                J
sixteen     bits~ showing        the value                             of                           <...
                                                                                                     c-
each bit:                                                                                            -

       ~
              '<I'
                     (',/     IO        Q:)     '<I'

       " 19f;j                                         Vi KJ r-./~
                                                       (',/       IO
                             g}
                                    ~         (:;
                     0\                                                              (',/
                                                                             '<I'   .....,   IO
       ~    r-./             '<I'             r-./                          IO               r-./    Q:)   '<I'   (',/    r-./



                                    I                         [                                     III
If ev e ry bit were to contain   a 1, the total  would be 65535. Thus
in 16 bits we can express    any value between O and 65535. Because
this kind of number does not let us express       negative   value$, we
call it an "unsigned    number."   We have been indicat i ng unsigned
numbers with the letter   "u" in our tables   and stack notations.
But what about negative          numbers?    In order to be able to express
a positive     or negative     number, we need to sacrifice      one bit that
will essentially      indicate      sign.   This bit is the one at the far
left, the "high-order       bit."     In 15 bits we can express a number as
high as 32767; When the sign bit contains              1, then we can go an
equal dista n ce back into the negative             numbers.  Thus witnin 16
bits we can r epresent          any number from -32768 to +32767.           This
should     look familiar     to you as the ra n ge of         single-length                         a
number, which we have been i nd i cating with the letter           "n."




                                    I 1                       III
tFor     Beginner           Beginners

If you are unfami l iar with binary notation,                                             ask someone              you know
who likes math, or find a book on computers                                              for beginners.
7 A NUMBER
         OF KINDSOF NUMBERS                                                           151




Before we leave you with any misconceptions,      we'd better clarify
the way negative    numbers are represented.     You might think that
it's a simple matter of setting the sign bit to indicate     whether a
number is positive or negative,   but it doesn't work that way.
To explain how negative     numbers are represented,   let's                 return    to
decimal notation     and examine a counter     such as that                  found     on
many tape recorders.

Let's say the counter has three digits.     As you wind the tape
forward, . the counter-wheels    turn and the number increases.
Starting  once again with the counter at 0, now imagine you're
winding the tape backwards.      The first number you see is 999,
which, in a sense, is the same as -1. The next number will be 998,
which is the same as -2, and so on.


                                                               003
                                                               002.
                                                               001
                                                               Q_OO

                                                             I ct"''
                                                             I" "'l
                                                             I ctct11
The representation      of signed   numbers in a computer            is similar.
Starting   with the number
     0000000000000000

and going backwards      one number, we get
     1111111111111111         (sixteen   ones)
which stands for 65535 in unsigned          notation         as well as for -1 in
signed notation. The number
     1111111111111110
which stands for 65534 in unsigned               notation,      represents         -2 in
signed notation.

Here's a chart that shows how a binary number on the stack can be
used either as an unsigned number or as a signed number:
152                                                          Starting       FORTH




                 as an
                unsigned
                 number
                  65535             1111111111111111

                   ...                     ...               as a
                                                            signed
                  32768             1000000000000000        number
                  32767             0111111111111111         ,j,t.   /0 /


                   ...                     ...                   ...
                         0          0000000000000000                   0
                                    1111111111111111                  -1

                                           ...                   ...
                                    1000000000000000        -32768


This bizarre-seeming      method for representing negative  values
makes it possible for the computer to use the same procedures for
subtraction   as for addition.
To show how this works, let's           take a very simple problem :
       2
      -1

Subtracting one from two is the same as adding two plus negative
one. In single-length  binary notation, the two looks like this:
       0000000000000010

while negative-one           looks like this:
       1111111111111111

The computer adds them up the same way we would on paper: that
is when the total of any column exceeds one, it carries  a one
into the next column. The result looks like this :
        0000000000000010
      + 1111111111111111
       10000000000000001

As you can      see, the computer had to carry a one into every
column all      the way across,    and ended up with a one in the
seventeenth     place.  But since the stack is only sixteen bits wide,
7 A NUMBEROF KINDS OF NUMBERS                                                               153




the result       is simply

        0000000000000001

which    is the correct         answer,      one.

We needn't   explain   how the computer converts                   a positive    number
to negative,    but we will tell   you that  the                  process     is called
"two's complementing."



Arithmetic       Shift


While we're on the subject       of how a computer   performs    certain
mathematical      operations,   we'll explain   what is meant by the
mysterious   phrases    back in Chap. 5: "arithmetic    left shift"    and
"arithmetic   right shift."


  A FORTH Instant            Replay:
  2*       (n      n*2)         Multiplies      by two (arithmetic       left     shift).

  2/       (n      n/2)        Divides       by two (arithmetic      right      shift).


To illustrate,       let's    pick     a number,    say six,   and write        it in binary
form:

        0000000000000110
(4 + 2). Now let's  shift              every     digit one place   to the           left,   and
put a zero in the vacant               place    in the one's column.
        0000000000001100
This is the binary     representation        of twelve   (8 + 4), which is
exactly   double the original     number.     This works in all cases, and
it also works in reverse.       If you shift     every digit  one place   to
the right   and fill the vacant       dig it with a zero, the result    will
always be half of the original        value.

In arithmetic       shift,  the sign bit does not get shifted.        This
means that a positive        number will stay positive    and a negative
number will stay negative       when you divide   or multiply  it by two.
(When the high-order       bit shifts with all the other bits, the term
is "logical   shift.")

The important   thing for you to know is that a computer can shift
dig its much more quickly  than it can go through all the folderol
of normal division    or multiplication.   When speed is critical,
154                                                     Starting    FORTH




it's   much better   to say
       2*
than
       2 *

and it may even be better       to say
       2* 2* 2*
than

       8    *
depending on your particular    model of computer,     but this    topic   is
getting too technical  for right now.


An Introduction      to Double-length    Numbers

 A double - length    number is just what you probably     expected    it
would be: a number that is represented       in thirty-two bits instead
 of sixteen.      Signed   double-length    numbers have a range of
.±_2,147
       ,483,647 (a range of over four billion) .




In FORTH, a double-length       number takes        the place   of two
rng e-length    numbers on the stack.     Operators    like !2SWAP! and
       1
 2DUP are useful either for double-length
single-length  numbers.
                                              numbers or for pairs of

One more thing we should explain:      to the non-FORTH-speaking
computer world, the term "word" means a 16-bit value, or two
bytes.  But in FORTH, "word" means a defined       command.    So in
order to avoid confusion,    FORTH programmers refer to a 16-bit
value as a "cell." A double-length  number requires two cells.
7 A NUMBEROF KINDS OF NUMBERS                                               155




Other Number Bases

As you get more involved in programming, you'll need to employ
other number bases besides      decimal  and binary,  particularly
hexadecimal   (base 16) and octal (base 8). Since we '11 be talking
about these two number bases later on in this chapter,      we think
you might like an introduction   now.
Computer people began using hexadecimal        and octal numbers for
one main reason:     computers think in binary and human beings
have a hard time reading long binary numbers. For people, it's
much easier  to convert    binary to hexadecimal      than binary to
decimal, because sixteen     is an even power of two, while ten is
not. The same is true with octal.     So programmers usually use hex
or octal to express the binary numbers that the computer uses for
things like addresses and machine codes.      Hexadecimal (or simply
"hex") looks strange at first since it uses the letters     A through
F.


     Decimal         Binary     Hexadecimal
         0             0000             0
         1             0001             1
         2             0010             2
         3             0011             3
         4             0100             4
         5             0101             5
         6             0110             6
         7             0111             7
         8             1000             8
         9             1001             9
        10             1010             A
        11             1011             B
        12             1100             C
        13             1101             D
        14             1110             E
        15             1111             F

Let's take a single-length     binary       number:
     0111101110100001
To convert this number to hexadecimal,            we first   subdivide   it into
four units of four bits each:
     I 0111 I 1011 I 1010 I 0001 I
then convert   each 4-bit unit to its hex equivalent:
156                                                             Starting      FORTH




or simply 7BAl.

Octal   numbers use only the numerals        O through      7. Because
nowadays most computers      use hexadecimal    representation,
we'll skip an octal conversion   example
We'll have more on conversions      in the          section     titled       "Number
Conversions" later in this chapter.


The ASCII Character        Set

If the computer uses binary notation      to store numbers, how does it
store   characters      and other symbols?     Binary,   again,  but in a
special code that was adopted as an industry standard many years
ago.     The code is called        the American     Standard    Code for
Information    Interchange   code, usually abbreviated    ASCII.
Table 7-1 shows each character           in the system        and its      numerical
equivalent, both in hexadecimal         and in decimal        form.
The characters          in the first        column (ASCII codes 0-lF hex) are
called     "control       characters"         because   they indicate     that the
terminal     or computer is supposed to do something                 like ring its
bell, backspace,         start a new line, etc.         The remaining characters
are called       "printing      characters"       because they produce visible
characters     including       letters,     the numerals zero through nine, all
available     symbols and even the blank space (hex 20). The only
exception      is DEL (hex 7F) which is a signal              to the computer to
ignore the last character             sent.

In Chap. l we introduced   the word IEMITI. !EMIT! takes an ASCII
code on the stack and sends it to the terminal        so that the
terminal will print it as a character. For example,
      65 EMIT A ok
      66 EMIT"""'if"'ok

etc.    (We're using the decimal,   rather than the             hex, equivalent
because that's    what your computer is most likely             expecting   right
now.)t-
Why not test    IEMITI on every     printing    character,     "automatically"?

        PRINTABLES        127 32 DO I EMIT SPACE LOOP 1

t For Experts
Why are you snooping        on the beginner's     section?
7 A NUMBEROF KINDS OF NUMBERS                                        157




           TABLE 7-1 -- ASCII CHARACTERS& EQUIVALENTS



Char Hex Dec      Char Hex Dec     Char Hex Dec      Char Hex Dec

NUL   00     0    SP   20    32    @     40   64                60    96
SOH   01     1         21    33    A     41   65     a          61    97
STX   02     2    II
                       22    34    B     42   66     b          62    98
ETX   03     3    #    23    35    C     43   67     C          63    99
EOT   04     4    $    24    36    D     44   68     d          64   100
ENQ   05     5    %    25    37    E     45   69     e          65   101
ACK   06     6    &    26    38    F     46   70     f          66   102
BEL   07     7         27    39    G     47    71    g          67   103
BS    08     8     (   28    40    H     48    72    h          68   104
HT    09     9    )    29    41    I     49    73    i          69   105
LF    0A    10    *    2A    42    J     4A    74    j          GA   106
VT    OB    11    +    2B    43    K     4B    75    k          GB   107
FF    oc    12         2C    44    L     4C    76    1          GC   108
CR    OD    13         2D    45    M     4D    77    m          6D   109
SM    OE    14         2E    46    N     4E   78     n          GE   110
SI    OF    15    I    2F    47    0     4F   79     0          GF   111
OLE   10    16    0    30    48    p     50   80     p          70   112
DCl   11    17    1    31    49    Q     51   81     q          71   113
DC2   12    18    2    32    50    R     52   82     r          72   114
DC3   13    19    3    33    51    s     53   83     s          73   115
DC4   14    20    4    34    52    T     54   84     t          74   116
NAK   15    21    5    35    53    u     55   85     u          75   117
SYN   16    22    6    36    54    V     56   86     V          76   118
ETB   17    23    7    37    55    w     57    87    w          77   119
CAN   18    24    8    38    56    X     58   88     X   78          120
EM    19    25    9    39    57    y     59   89     y   79          121
SUB   lA    26         3A    58    z     SA   90     z   7A          122
ESC   lB    27         3B    59    [     SB   91     {   7B          123
FS    lC    28    <    3C    60    \     SC   92         7C          124
GS    1D    29    =    3D    61    l     5D   93     }I 7D           125
RS    lE    30    >    3E    62          SE   94         7E          126
us    lF    31    ?    3F    63          SF   95     DEL 7F          127
                                                         (RB)




The "Char" columns list the ASCII characters     (some of which are
control    characters);   the "Hex" columns give the hexadecimal
equivalents;     and the "Dec" columns present the decimal equiva-
lents.
158                                                                                       Starting      FORTH




PRINTABLES will emit every printable                                  character   in the ASCII set:
that is, the characters  from decimal                                  32 to decimal    126. (We 're
using the ASCII codes as our ~ loop                                  index.)

      PRINTABLES          !   II   # $      % &     I     (   )     * + • • ,~
Beginners   may be interested    in some of the                                 control     characters         as
well.   For instance,  try this:



              ~
      7 EMIT ok

You should   have        heard   some sort                        of beep,       which is the video
terminal's version        of the mechanical                         printer's     "typewriter bell."

Other control       characters               that         are        good       to   know     include     the
following:

                                                         decimal
      name        oeeration                             eg:uivalent

       BS         backspace                                         8

       LF         line   feed                                      10
       CR         carriage         return                          13

Experiment    with these           control        characters,               and see what they            do.

ASCII is designed    so that each character   can be represented     by
one byte.   The tables   in this book use the letter "c" to indicate
a byte value that is being used as a coded ASCII character.



Bit   Logic


The words !AND! and ~ (which we introduced            in Chap. 4) use "bit
logic":   that is, each bit is treated    independently,      and there are
no "carries"    from one bit,pljce    to the next.       For example,  let's
see what happens when we AND these two binary numbers:

      0000000011111111
      0110010110100010 !AND!
      0000000010100010
For any result-bit       to be "l,"   the respective      bits in both
arguments must be "l."      Notice in this example that the argument
on top contains    all zeroes in the high-order    byte and all ones in
7 A NUMBER OF KINDS OF NUMBERS                                                                             159




the low-order    byte.    The effect on the second argument in this
example    is that the low-order      eight  bits are kept but the
high-order    eight    bits are all set to zero.     Here the first
argument is being used as a "mask, to mask out the high-order   11


byte of the second argument.
The word [Qg[also uses bit logic.                          For example,
         1000100100001001
         0000001111001000 @Bl
         1000101111001001
a "l" in either   argument produces  a "l" in the result.                                            Again,
each column is treated separately,  with no carries.

By clever use of masks, we couid even use a 16-bit value to hold
sixteen  separate flags. For example, we could find out whether
this bit
         1011101010011100
                         ..
is "l" or       11
                     0" by masking out all other                      flags,     like this:
         1011101010011100
         0000000000010000 !AND!
         0000000000010000
Since     the    bit    was   "1,"    the         result   is    "true."         Had   it   been   "0,"    the
result     would have been "0 II or "false."
We could set the flag                to     11
                                                 0" without          affecting     the other       flags    by
using this technique:
         1011101010011100
         1111111111101111 IANDI
         1011101010001100
                         ..
We used a mask that contains all  l s except  for the bit we     11    11


wanted to set to 0." We can set the same flag back to "l" by
                              11


using this technique:
         1011101010001100
         0000000000010000 @Bl
         1011101010011100
                         ..
160                                                             Starting        FORTH




                          SECTION II -- FOR EVERYBODY



Signed     and Unsigned      Numbers

Back in Chap.        l we introduced     the   word INUMBERj.




If the word IINTERPRETI can't          find an incoming    string    in the
dictionary,     it hands it over to the word IN-UMBER!. [NUMBER!then
attempts     to convert  the string   into a number expressed     in binary
form.     If [NUMBERjsucceeds,     it pushes the binary  equivalent     onto
the stack.

NUMBER does not do any                 range-checking.    t  Because       of    this,
NUMBE can convert either               signed or unsigned   numbers.

For instance,    if you enter  any number between    32768 and 65535,
[NUMBER! will    convert   it as an unsigned    number.     Any value
between    -32768 and -1 will    be stored   as a two's-complement
integer.

This is an important       point:     the stack can be used to hold either
signed      or unsigned      integers.         Whether   a binary    value    is
interpreted      as signed   or unsigned      depends  on the operators    that
you apply      to it.    You decide      which form is better     for a given
situation,    then stick to your choice.




tFor     Beginners

This means that [NUMBER!does not check whether      the number you've
entered   as a single-length    number exceeds the proper   range.  If
you enter a giant number, INUMBERIconverts      it but only saves the
least significant    sixteen digits.
7 A NUMBER OF KINDS OF NUMBERS                                                          161




We've introduced       the word    G],which   prints      a value    on the stack        as
a signed number:

       65535 . -1 ok
The word [Q:Jprints       the same binary      representation          as an unsigned
number:

       65535 u. 65535 ok


  u.                   (u --   )               Prints    the  unsigned
                                               sing le-length    number,
                                               followed by one space.

In this book the letter   "n" signifies       signed single-length
numbers, while the letter    "u" signifies         unsigned   single-
length   numbers.   (We've already       introduced       M, which
prints  an unsigned   number right-justified         within  a given
column width.)


Here is a table    of additional       words that       use unsigned         numbers:


  U*                   (ul u2 -- ud)           Multiplies      two 16-bit
                                               numbers.         Returns     a
                                               32-bit     result.       All
                                               values      are   unsigned.

  U/MOD                (ud ul -- u2 u3)        Divides    a )2-bit     by a
                                               16-bit number.       Returns
                                               a 16-bit    quotient     and
                                               remainder.      All values
                                               are unsigned.
  U<                   (ul u2 -- f)            Leaves true if ul < u2,
                                               where both are treated
                                               as 16-bit   unsigned
                                               integers.

  DO •.. /LOOPt        DO: (u-lim i t          Like DO ..• +LOOP ex-
                           u-index --          cept uses an unsigned
                       /LOOP: (u -    )        limit,     index,  and
                                               increment.




tFORTH-79 Standard
!/LOOP! is included      in the optional      Reference      Word Set.
162                                                                      Starting      FORTH




1/LOOPI is similar  to l+LOOPI, in that it terminates     a [QQ}loop and
that it takes an incrementing     value.   The difference    is that with
1/LOOPI, the index and limit
increment   must be positive.
                                        iiy
                                     rarge from zero to 65535, and the
                                  LOOP executes    somewhat faster   than
!+LOOP!.


Number Bases

When you first   load FORTH, all number                  conversions           use base    ten
(decimal) for both input and output.




                     CURRENT
                      BASE

                         ~



You can easily   change        the base       by executing        one of the following
comands:


  HEX                                                Sets the base        to sixteen.
  OCTAL                                              Sets the       base to eight
                                                     (available       on some sys-
                                                     tems).t
  DECIMAL            (    --      )                  Returns   the base        to ten.




tFor   Experts

!OCTAL! is omitted       unless       the   design    of the      particular        processor
compels its use.
7 A NUMBEROF KINDS OF NUMBERS                                                               163




When ·you change   the number base, it stays chan ed until you
change   it again.   So be sure to declare  DECIMAL as soon as
you're done with another number base.t

These     commands    make       it     easy     to    do   number        conversions          in
"calculator   style."
For example,     to convert      decimal        100 into     hexadecimal,        enter

       DECIMAL 100 HEX • 64 ok

To convert      hex F into    decimal          (remember        you are    already      in hex),
enter

       OF DECIMAL . 15 ok

Make it a habit,  starting            right    now, to precede            each   hexadecimal
value with a zero, as in
       0A OB OF

This practice avoids mix-ups with such predefined                           words as ~,        [Q],
or~   in the EDITOR vocabulary.




                                 A Handy Hint
                  A Definition         of BINARY -          or Any-ARY


  Beginners  who want to see what numbers                         look    like   in binary
  notation  may enter this definition:

         : BINARY     2 BASE ! ;

  The new word BINARY will operate     just like [OCTAL[or [HEX! but
  will change the number base to two. On systems which do not
  have the word IOC~~1], experimenters    may define
         : OCTAL     8 BASE ! ;




tFor   People    Using Multiprogrammed                Systems

When you change the number base, you change it for your terminal
task only. Every terminal task uses a separate number base.
164                                                              Starting         FORTH




 Double-length          Numbers
 Double-length   numbers provide    a range of +2,147,483,647.  Most
 FORTH systems support double-length      numbers to some degree.tt
 Normally, the way to enter a double-length    number onto the stack
 (whether from the keyboard or from a block) is to punctuate        it
 with one of these five punctuation   marks:
       I   •   I - :
 For example,          when you type
       200 ,OOOmI!Jl13




                              ,ooo


 INUMBERjrecognizes              the comma as a signal   that   this     value     should
 be   converted         to   double-length.    !NUMBER! then    pushes      the     value
 onto the stack as two consecutive              "cells" (cell   is the FORTH term
 for sixteen bits), the high order            cell on top.




 tFor polyFORTH Users:
 polyFORTH       includes     double-length  routines,     but they are
 "electives,"      which means that they are written     in the group of
 blocks which you must load each time the system is booted.          This
 arrangement       gives you the flexibility     to either    load these
 routines     or delete   them from your load block, according     to the
 needs of your application.
 t FORTH-79 Standard
 The Standard      requires    only three    double-length   arithmetic
 primitives.    The optional       Double Number Word Set includes many
 more double-length     operators.
7 A NUMBER OF KINDS OF NUMBERS                                                165




The FORTH word [Q:Jprints            a double-length      number without      any
punctuation.

  D.                  (d -     )                Prints     the signed~-
                                                double-length    number,     dot
                                                followed by one space.




In this    book, the letter        "d" stands    for a double-length       signed
integer.
For example, having entered a double-length     number, if you were
now to execute @:J, the computer would respond:
       D. 200000 ok

Notice that all of the following          numbers are converted        in exactly
the same way:

       12345. D. 12345 ok
       123.45 D. 12345 ok
       1-2345 D. 12345 ok
       1/23/45 D. 12345 ok
       1:23:45 D. 12345 ok .

But this   is not the same:
       -12345
because       this   value  would be converted        as a negative,
single-length      number. (This is the only case in which a hyphen
is interpreted     as a minus sign and not as punctuation.)
In the next section    we'll show you how to define                     your own
equivalents to 00:J
                  which will print whatever punctuation                  you want
along with the number.
166                                                                                 Starting       FORTH




Number Formatting             -    Double-length              Unsigned t


       $200.00          12/31/80           372-8493           6:32:59        98.6

The above numbers represent      the kinds                            of output      you can create
by defining    your own "number-formatting                              words"      in FORTH. This
section   will show you how.

The simplest        number-formatting                definition         we could     write     would be

       : UD.       <#    #S       #>     TYPE;

UD. will print      an unsigned       double-length     number.      The words @]
 and [!:g (respectively               pronounced        bracket-number           and
number-bracket)         signify      the beginning         and the end of the
number-conversion           process.       In this    definition,       the entire
conversion    is being performed         by the single word lifil (pronounced
numbers).       !#Si converts        the value      on the stack        into   ASCII
characters.      It will only produce as many digits              as are necessary
to represent      the number; it will not produce leading              zeroes.    But
it always produces        at least     one dig it, which will be zero if the
value was zero.       For example:

       12,345 UD. 12345ok
       12. UD. 12ok ·
       0 UD. Ook

The word !TYPE! prints                 the characters          that     represent      the     number at
your   terminal.         Notice         that     there   is    no space      between         the     number
~e           "ok."    To get             a space,        you would         simply      add     the    word
~,         like this:

       : UD.       <# #S #>            TYPE SPACE;

Now let's say we have a phone number on the stack,                                    expressed        as a
32-bit unsigned integer. For example, we may have                                    typed in

       372-8493

(remember     that    the hyphen  tells   !NUMBER! to treat   this  as a
double-length      value). We want to define a word which will format
this value back as a phone number.        Let's call it .PH# (for "print
the .E!!_one number") and define   it thus:



tFor Those Whose Systems                       Do Not Have Double-length               Routines
  Loaded

The examples used in this and the next section     won't do what you
expect.    The principles   remain the same, however, so read these
two sections   carefully, then read the note on page 172.
7 A NUMBER
         OF KINDSOF NUMBERS                                                                  167




      : ,PH#      <# # # # # 45 HOLD #S #> TYPE SPACE
Our definition          of .PH# has
everything   that UD. has, and more.
The FORTH word I!] (pronounced
number) produces       a single    digit
only.      A number-formatting
definition     is reversed     from the
order in which the number will be
printed, so the phrase


produces the right-most             four digits
of the phone number.
Now it's time to insert the hyphen.    Looking up the ASCII value
for hyphen in the table     in the beginner's    section     of this
chapter, we find that a hyphen is represented  by decimal 45. The
FORTH word IHOLDJtakes this ASCII code and inserts       it into the
formatted number character string.
We now have three        digits     left.          We might use the phrase


but it's     easier    to simply   use the word j#SI, which                                 will
automatically     convert the rest of the number for us.
If   you    are   more   familiar           with     ASCII   codes       represented           in
hexadecimal       form, you can use this definition                  instead:
      HEX : .PH#         <# # # # # 2D HOLD #S #> TYPE SPACE
      DECIMAL
Either     way, the compiled definition                will be exactly          the same.

Now let's format an unsigned                  double-
length   number as a date,                    in the                 'i1®0£i1a~
following form:


                                                                     ~
                                                                           y
      7/15/80

Here is the definition:

      : .DATE      <# # # 47 HOLD # # 47 HOLD #S #>                             TYPE SPACE ;
Let's follow the above definition,                    remembering      that     it is written
in reverse order from the output.                    The phrase
168                                                                     Starting       FORTH




       # # 47 HOLD
produces     the right-most        two digits     (representing     the year) and
the right-most        slash.      The next occurrence         of the same phrase
produces     the middle two d0.,!ts          (representing      the day) and the
left-most     slash.     Finally,    ~ produces        the left-most    two digits
(representing      the month).

We could    have   just    as easily     defined
       # # 47 HOLD
as its own word           and used     this    word   twice    in the     definition      of
.DATE.

Since you have control         over the conversion     process,   you can
actually   convert   different     digits in different   number bases,    a
feature  which is useful in formatting       such numbers as hours and
minutes.   For example, let's say that you have the time in seconds
on the stack,    and you want a word that will print        hh:mm:ss.  You
might define it this way:
        SEXTAL 6 BASE I 7 t
        :00  # SEXTAL # DECIMAL 58 HOLD 7
        SEC   <i :00 :00 iS i> TYPE SPACE 7
We will use the word :00 to format                   the
seconds     and the minutes.       Both seconds and
minutes     are modulo-60,       so the right     digit
can go as high as nine, but the left digit
can only         go up to five.         Thus in the
definition      of :00 we convert     the first digit
(the one on the right)         as a decimal    number,
then go into "sextal"          (base 6) and convert
the left       digit.    Finally,      we return       to
decimal      and insert    the colon      character.
After     :00 converts      the seconds       and the
minutes, I!§] converts      the remaining     hours.

For example,   if we had 4500 seconds                 on the
stack, we would get

       4500. SEC 1:15:00 ok

Table 7-2 summarizes   the FORTH words that
are used in number formatting.      (Note the
"KEY" at the bottom,      which serves   as a
reminder of the meanings of "n," "d," etc.)

tFor   Beginners
See the Handy Hint on page              163.
7 A NUMBER OF KINDS OF NUMBERS                                                                169




                   TABLE       7-2 -- NUMBER FORMATTING


  <#                     Begins     the number         conversion              process.
                         Expects an unsigned          double-length            number on
                         the stack.                                         l brQc~et- nurnber
                                                                                  1.                )


  #                      Converts     one digit      and puts it into      an
                         output   character     string.    [ID always pro-
                         duces a digit--if     you're   out of significant
                         digits,  you'll still  get a zero for every [ID.
                                                                                   {....:n==u"-rri..,..,b-er.,,...
                                                                                             /
  #S                     Converts the number until
                         Always produces ~ least
                                                                  the result
                                                                 one digit
                                                                                is zero.
                                                                               (0 if the
                                                                                              I
                         value is zero).                                          ( numbersi
  c HOLD                 Inserts,   at the current       position      in the
                          character     string     being    formatted,        a
                         character   whose ASCII value is on the stack.
                         jHOLDI (or a word that uses IHOLDI) must be
                         used between~        and lli2].
  SIGN                   Inserts   a minus sign in the output string    if
                         the third     number on the stack is ~ative.
                         Usually    used immediately   before ut2.] for a
                         leading   minus sign.

  #>                     Completes      number     conversion  by leaving  the
                         character       count     and address   on the stack
                          (these  are    the     appropriate          arguments         for
                         jTYPEI).                                           {nvmber- brac~ct

                                                                                               )'
Stack    effects   for      number formatting
                                                                                       ~'
  phrase                 stack                      ~ of           arguments

  <# ••• # >             (d -- adr u) or            32-bit       unsigned
                         (u O -- adr u)             16-bit       unsigned

  <# ••• SIGN # >        (n !di -- adr u)           32-bit signed  (where n is
                         or                         the high-order   cell of d
                                                    and Id! is the absolute
                                                    value of d).

                         (n lnl O -- adr u)         16-bit signed (where jnj is
                                                    the absolute  value).

  KEY

  n, nl ••.        16-bit     signed numbers                 adr      address
  d, dl, .••       32-bit     signed numbers                 C        ASCII char-
  u, ul, .•.       16-bit     unsigned numbers                        acter value
170                                                        Starting   FORTH




Number Formatting     -   Signed   and Single-length

So far we have formatted   only unsigned double-length numbers.
The [311•• -~ form expects only unsigned double-length numbers,
but we can use it for other types of numbers by making certain
arrangements on the stack.
For instance,   let's look at a simplified    version of the system
definition  of [g;] (which prints a signed double-length number):
      : D.     SWAP OVER DABS <# #S SIGN #>            TYPE SPACE ;
The word !SIGN!, which must be situated within the 8!] ... ~ phrase,
inserts    a minus sign in the character   string only if the third
number on the stack is negative.       So we must put a copy of the
high-order    cell (the one with the sign bit) at the bottom of the
stack, by using the phrase
      SWAP     OVER




                 hi.9h
                 low




Because 81] expects only unsigned double-length     numbers, we must
take the absolute value of our double-length    signed number, with
the word !DABS!. We now have the proper arrangement of arguments
on the stack for the EJ]... [g phrase.  The word !SIGN!, like IHOLDI,
will insert the minus sign at whatever point within the character
string we situate  it.  Since we want our minus s~      to appear at
the left, we include !SIGN! at the right of our l5Jtj ••• ~ phrase.
In some cases, such as accounting,   we may want a negative    number
to be written
      12345-
in which case we would place         the word ISIGNI at the left      side   of
our @[I... ~ phrase, like this:
7 A NUMBER
         OF KINDSOF NUMBERS                                               171




        <# SIGN #S #>
Let's define    a word which will print   a signed
double-length    number with a decimal point and
two decimal places to the right of the decimal.
Since    this is the form most often
writing dollars
                                         used for
                   and cents, let's call it .$ and
define it like this:
         .$     SWAP OVER DABS
                                                                    $
              <# # # 46 HOLD #S SIGN 36 HOLD #> TYPE SPACE
Let's    try it:
        2000.00 .$ $2000.00 ok

or even
        2,000.00 .$ $2000.00 ok

We recommend that       you save   .$,   since   we'll   be using   it in some
future examples.
You can also write special formats for single-length    numbers. For
example, if you want to use an unsigned single-len~          number,
simply put a zero on the stack before         the word ~-        This
effectively      changes    the single-length        number  into     a
double-length   number which is so small that it has nothing (zero)
in the high-order cell.
To format a signed single-length    number, again you must supply a
zero as a high-order  cell.   But you also must leave a copy of the
signed number in the third stack position for ISIGNI, and you must
leave the absolute    value of the number in the second stack
position.  The phrase to do all of this is
        DUP ABS 0
172                                                                          Starting      FORTH




Here are the "set-up"               phrases   that     are     needed       to print      various
kinds of numbers:



        Number to be printed                          Precede       @n by
        32-bit,     unsigned                          (nothing      needed)

        31-bit,     plus sign                         SWAP OVER DABS
                                                        (to save the sign in the
                                                        third   stack position for
                                                        ISIGNi)

        16-bit,     unsigned                          0
                                                             (to    give        a       dummy
                                                             high-order      part)

        15-bit,     plus   sign                       DUP ABS 0
                                                        (to save           the sign)




 If Your System            Does Not Have Double-length               Routines          Loaded
In    this   case    the   set-up   phrases   are    different,      as     follows:


        Number to be printed                          Precede       @n by
        16-bit,     unsigned                          DUP

        15-bit,     plus sign                         DUP ABS DUP


Even though [ID still      expects    two cells   on the stack,    in this
case the significant       cell   must be on .!Q..p_ (where normally    the
high-order    cell   is found).    The contents     of the second    stack
position   are not used.
7 A NUMBER OF KINDS OF NUMBERS                                                          173




Double-length    Operators

Here is a list   of double - length         math operators:t      t

  D+                 (dl d2 -- d-sum)            Adds two 32-bit        numbers.
                                                                              _d,__-,--
  D-                 (dl d2 -      d-diff)        Subtracts    two 32-bit
                                                  numbers (dl-d2)-.    -.-...__,/

  DNEGATE            (d --   -d)                  Changes the sign
                                                  32-bit number.
  DABS               (d -- ldl)                   Returns
                                                  value
                                                  number.
  DMAX               (dl d2 -- d-max)             Returns the maximum of
                                                  two 32-bit numbers.
  DMIN               (dl d2 -- d-min)             Returns the minimum
                                                  two 32-bit numbers.
  D=                 (dl d2 -- f)                 Returns true        if dl
                                                  d2 are equal.
  DO=                (d --   f)


  D<                 (dl   d2 -    f)             Returns   true       if
                                                  less than d2.             ---       ........
                                                                                           ~/
  DU<                (udl ud2 -- f)               Returns true if udl is
                                                  less   than ud2.    Both
                                                  numbers are unsig,~n~e~d~-~-~~
                                                                            -u - c~s-thal'I
  D.R                (d width --        )        Prints the signed JL- b1t
                                                 number, right-justified
                                                 within the field width.




tFor polyFORTH Users
The double-length     routines      must be loaded.
tFORTH-79 Standard
Except for lli±],~, and IDNEGATEI,which are required,                       these    words
are part of the optional Double Number Word Set.
174                                                                  Starting       FORTH




The initial   "D" signifies      that these operators    may only be used
for double-    engjh    operations,      whereas the initial     "2," as in

either
                1
l2SWAPI and 2DUP, signifies
         for double-length
                                     that these  operators
                                 numbers or for pairs
                                                               may be used
                                                         of single-length
numbers.

Here's   an example        using    IQ±]:
       200,000 300,000          D+ D, 500000 ok

A warning      for experimenters:        you can write    definitions       that
contain     double-precision      operators,    but you cannot       include     a
punctuated,     double-precision     number inside    a definition.       In the
next chapter      we'll explain   what to do instead.



Mixed-Length         Operators


Here's   a table   of very useful   FORTH words which operate                        on a
combination    of single- and double-length  numbers: t

  M+           (d n -- d-sum)             Adds      a 32-bit     number   to a
                                          16-bit    number.    Returns a 32-bit
                                          result,

  M/           (d n -- n-quot)            Divides   a 32-bit     number by a
                                          16-bit number.     Returns a 16-bit
                                          result.  All values are signed.

  M*           (nl n2 -         d-prod)   Multiplies   two 16-bit numbers.
                                          Returns    a 32-bit result.  All
                                          values are signed.
  M*/          (d    n n --               Multiplies              a 32-bit             rn-
                    d-result)             number by a 16-bit number and               star-
                                          divides      the   triple-length            <:.lash
                                          result     by a 16-bit         number
                                           (d*n/n).      Returns       a 32-bit
                                          result.    All values are signed.




t FORTH-79 Standard
The mixed-length    operators  are not                    included    in   either     the
Required or the Double Number Word Set.
7 A NUMBER
         OF KINDSOF NUMBERS                                                                  175




Here's      an example           using~:

         200,000 7 M+ D. 200007 ok

Or, using ~,                we can redefine      our earlier         version     of % so that
it will accept             a double-length     argument:
            %        100 M*/ ;

as in

         200.50 15 % D. 3007 ok

If you have            loaded the definition        of.$    which we gave         in the last
Handy Hint,            you can enter

         200.50 15 % .$ $30.07 ok

We can redefine      our earlier    definition                 of R% to get           a rounded
double-length   result,  like this:

            R%        10 M*/     5 M+ 10 M/ ;

then

         987.65 15 R% .$ $30.08 ok

Notice   that  IM*fl is                the only ready-made             FORTH word which
performs multipilcation                  on a double-length         argument. To multiply
200,000         by    3,   for    instance,   we   must    supply      a   "l"   as    a dummy
denominator:

        200,000 3 1 M*/ D. 600000 ok
since
        3
        T
is the same as 3.

!~*/I is also    the only ready-made      FORTH word that     performs
division   with a double-length   result.   So to divide  200,000 by 4,
for instance,   we must supply a "l" as a dummy numerator:

        200,000 l 4 M*/ D. 50000 ok
176                                                         Starting   FORTH




Numbers in Definitions

When a definition   contains    a number, such as
      : SCORE-MORE 20 + :
the number is compiled     into the dictionary       in binary   form, just as
it looks on the stack.




The number's binary value      depends on the number base at the time
you compile the definition.       For example, if you were to enter
      HEX      SCORE-MORE 14 + :           DECIMAL
the dictionary  definition   would contain   the hex value 14, which
is the same as the decimal        value  20 (16 + 4).   Henceforth,
SCORE-MOREwill always add the equivalent        of decimal 20 to the
value on the stack, regardless   of the current number base.
If, on the other hand, you were to put the word iHEXI inside the
definition,  then you would change   the number base when you
execute the definition.
For example,   if you were to define:
      DECIMAL
      : EXAMPLE HEX 20 .       DECIMAL;
the numbefi would re compiled as the binary equivalent            of decimal
20, since _DECIMAL.was current at compilation time.
At execution   time, here's    what happens:
      EXAMPLE14 ok
The number is output     in hexadecimal.
7 A NUMBER
         OF KINDSOF NUMBERS                                                    177




For the record,         a number that appears inside  a definition is
called     a "literal."       (Unlike the words in the rest of the
definition     which allude to other definitions,    a number must be
taken literally.)
Here is a list   of the FORTHwords we've covered          in this    chapter:

Unsigned operators
  u.                 (u --               Prints      the unsigned
                                         single-length       number,
                                         followed by one space.
  U*                 (ul u2 -- ud)       Multiplies    two 16-bit num-
                                         bers.      Returns  a 32-bit
                                         result.     All values   are
                                         unsigned.
  U/MOD              (ud ul -- u2 u3)    Divides a 32-bit by a 16-
                                         bit number.        Returns     a
                                         16-bit    quotient    and re-
                                         mainder.      All values   are
                                         unsigned.
  U<                 (ul u2 -- f)        Leaves    true if ul < u2,
                                         where both are treated    as
                                         16-bit unsigned integers.
  DO ••• /LOOP       DO:      (u-limit    Like   DO •••    +LOOP      except
                         u-index --      uses an unsigned      limit,
                     /LOOP: (u -- )      index, and increment.
Number bases
  HEX                                     Sets the base to sixteen.
  OCTAL                                   Sets the     base to eight
                                          (available     on some sys-
                                          tems).
  DECIMAL            (     -- )           Returns the base to ten.
Number formatting        operators
  <#                 Begins     the number conversion               process.
                     Expects an unsigned double-length              number on
                     the stack.
                     Converts one digit anuuts       it into an output
                     character     string.   L!J always produces       a
                     digit--if   you're out of significant     digits,
                     you'll still get a zero for every [fil.
178                                                                      Starting        FORTH




  ts                    Converts  the number until                the   result     is zero.
                        Always produces  ~ least                  ~ digit         (0 if the
                        value is zero).
  c HOLD                Inserts,  at the current     position      in the
                        character string  being formatted,    a character
                        whose ASCII value is on the stack.     !HOLDI(or a
                        word that uses !HOLDI)must be used between E!J
                        and~-
  SIGN                  Inserts   a minus sign in the output     string   if
                        the third     number on the stack    is re,ative.
                        Usually    used immediately   before     #> for a
                        leading minus sign.

  #>                    Completes    number conversion                  by leaving  the
                        character     count and address                   on the stack
                        (these    are the appropriate                   arguments   for
                        !TYPEI).
Stack   effects   for    number formatting

  phrase                stack                      ~ of           arguments
  <# ... #>             (d -- adr u) or            32-bit    unsigned
                        (u O - adr u)              16-bit    unsigned
  <# ... SIGN #>        (n jaj -       adr u)      32-bit signed              (where     n is
                        or                         the high-order               cell     of d
                                                   and      ldl    is   the      absolute
                                                   value     of d).

                        (n lnl O -- adr u)         16-bit  signed    (where             lnl is
                                                   the absolute   value).

Double-length     operators           (Optional   in FORTH-79 Standard)
  D+                    (dl d2 -- a-sum)           Adds two 32-bit            numbers.

  D-                    (dl d2 -        d-diff)    Subtracts        two              32-bit
                                                   numbers (dl-d2).

  DNEGATE               (d -    -d)                Changes    the             sign      of      a
                                                   32-bit number.

  DABS                  (d -    ldl)               Returns the absolute                 value
                                                   of a 32-bit number.

  DMAX                  (dl d2 -        a-max)     Returns the maximum of two
                                                   32-bit numbers.
7 A NUMBEROF KINDS OF NUMBERS                                                        179




 DMIN               (dl d2 -- a-min)             Returns the minimum of two
                                                 32-bit numbers.

 D=                 (dl d2 -- f)                 Returns true      if dl and d2
                                                 are equal.
 DO=                (d -- f)                     Returns true if dis       zero.
 D<                 (dl d2 -- f)                 Returns true      if dl is less
                                                 than d2.
 DU<                (udl ud2 -- f)               Returns true if udl is less
                                                 than ud2. Both numbers are
                                                 unsigned.
 DU<                                             Prints the signed         32-bit
                                                 number, followed         by one
                                                 space.
 D.R                (d width --        )         Prints  the signed         32-bit
                                                 number,    right-justified
                                                 within the field width.

Mixed-length    operators       (Not required        by FORTH-79 Standard)
 M+                 (d n -- d-sum)               Adds a 32-bit number to a
                                                 16-bit number.  Returns a
                                                 32-bit result.
 M/                 (d n -- n-quot)              Divides a 32-bit number by
                                                 a 16-bit number. Returns a
                                                 16-bit result.   All values
                                                 are signed.
 M*                 (nl n2 -- d-prod)            Multiplies       two 16-bit
                                                 numbers.     Returns a 32-bit
                                                 result.      All values   are
                                                 signed.
 M*/                (d n n --                    Multiplies    a 32-bit number
                      d-result)                  by a 16-bit       number     and
                                                 divides    the triple-length
                                                 result   by a 16-bit number
                                                 (d*n/n).     Returns a 32-bit
                                                 result.      All values      are

 KEY
 n, nl           16-bit signed numbers                 b      8-bit byte
 d, dl, •••      32-bit signed numbers                 f      Boolean flag
 u, ul, ••.      16-bit unsigned numbers               c      ASCII character
                                                              value
 ud, udl, •••    32-bit     unsiqned       numbers      adr   address
180                                                          Starting   FORTH




Review of Terms


Arithmetic     left
and right     shift   the process      of shifting   all bits in a number,
                      except     the sign bit, to the left      or right,   in
                      effect      doubling      or halving    the   number,
                      respectively.

ASCII                 a standardized        system of representing      input/
                      output characters        as byte values.    Acronym for
                      American       Standard      Code for Information
                      Interchange.       (Pronounced   ask-key.)

Binary                number base    2.
Byte                  the standard    term for an 8-bit     value.

Cell                  the FORTH term for a 16-bit       value.

Decimal               number base    10.
Hexadecimal           number base 16.

Literal               in general,  a number or symbol which represents
                      only itself:    in FORTH, a number that appears
                      inside a definition.
Mask                  a value   which   can be "superimposed"      over
                      another,   hiding   certain bits and revealing
                      only those bits that we are interested  in.
Number
formatting            the process   of printing  a number, usually        in a
                      soecial  form such as 3/13/81 or $47.93.
Octal                 number base    8.
Sign bit,
high-order     bit    the bit which, for a siqned       number, indicates
                      whether  it is positive     or neqative   and, for an
                      unsiqned   number,    represents      the bit of the
                      highest  magnitude.

Two's
complement            for any number, the number of equal absolute
                      value but opposite    siqn.    To calculate 10 - 4,
                      the computer    first produces   the two's comple-
                      ment of 4 (i.e., -4), then computes 10 + (-4).

Unsigned     number   a number which       is assumed to be positive.
7 A NUMBER
         OF KINDSOF NUMBERS                                                           181




Unsigned single-
length number             an integer   which    falls   within      the   range      Oto
                          65535.

Word                      in FORTH,    a defined    dictionary                entry;
                          elsewhere, a term for a 16-bit value.



Problems     -- Chapter     7

FOR BEGINNERS

1.     Veronica    Wainwright    couldn't   remember the upper limit for a
       signed   single-length      number, and she had no book to refer
       to, only a FORTH terminal.         So she wrote a definition  called
       N-MAX, using      a IBEGINI••• IUNTILI loop.  When she executed     it,
       she got

            32767 ok

       What was her definition?

2.     Since   you now know that          !ANDI and !ORI ei;!!.P,J.oy bit         logic,
       explain  why the following        example must use lQSj instead             of  EJ:
              MATCH HUMOROUSSENSITIVE AND
                ART-LOVING MUSIC-LOVING OR AND SMOKING NOT AND
                  IF • 11 I HAVE SOMEONEYOU SHOULD MEET " THEN ;
3.     Write a definition    that "rings"    your terminal's     bell three
       times.    Make sure that there    is enough of a delay        between
       the bells   so that they are distinguishable.         Each time the
       bell rings,   the word "BEEP" should appear        on th~ terminal
       screen.


(Problems    4 and 5 are practice        in double-length        math.)

4.     a. Rewrite the temperature       conversion     definitions  which you
          created     for the problems      in Chap. 5. This time assume
          that    the input     and resulting      temperatures    are to be
          double-length       signed   integers     which are scaled      (i.e.,
          multiplied)      by ten.    For example,        if 10.5 degrees       is
          entered,    it is a 32-bit integer    with a value of 105.

       b. Write    a formatted     output word named .DEG which will
          display    a 32-bit signed integer  scaled  by ten as a string
          of digits,   a decimal point, and one fractional   digit.

           For example:

             12.3 .DEGtlJI!llm 12.3 ok
182                                                                    Starting     FORTH




Problem    4, continued

      c. Solve    the following    conversions:
              o.o° F in Centigrade
            212.0° F in Centigrade
             20.5° F in Centigrade
             16.0° c in Fahrenheit
            -40.0° C in Fahrenheit
            100.0° K in Centiqrade
            100.0° K in Fahrenheit
            233.0° K in Centiqrade
            233,0° K in Fahrenheit

5.    a. Write    a routine   which    evaluates    the quadratic            equation
            7x 2 + 20x + 5

          given   x, and returns      a double-length        result.
      b. How larqe   an x will work without              overflowing           thirty-two
         bits as a signed number?


FOR EVERYONE


6.    Write a word which prints          the numbers 0 through 16 (decimal)
      in decimal, hexadecimal,           and binary  form in three columns.
      E.g.,
            DECIMAL 0         HEX 0      BINARY          0
            DECIMAL 1         HEX 1      BINARY          1
            DECIMAL 2         HEX 2      BINARY         10

            DECIMAL 16        HEX 10     BINARY 10000

7.    If you enter

            ..mrmm
      (two periods    not separated             by a space)            and   the    system
      responds  "ok," what does this          tell you?

8.    Write a definition     for a phone-number formatting word that
      will also print the area code with a slash if and only if the
      number includes    an area code.   E.g.,

            555-1234 .PH# 555-1234 ok
            213/372-8493 • PH# 213/372 - 8493 ok
                   8   VARIABLES, CONSTANTS, AND ARRAYS


As we have seen throughout         the previous   seven chapters,   FORTH
programmers use the stack to store numbers temporarily         while they
perform    calculations    or to pass arguments        from one word to
another.       When programmers         need to store      numbers  more
permanently,    they use variables    and constants.
In this chapter,    we'll learn      how FORTH treats  variables    and
constants,   and in the process      we'll see how to directly   access
locations  in memory.


Variables

Let's start with an example of a situation   in which you'd want to
use a variable--to   store the day's date.t    First we'll create  a
variable   called DATE. We do this by saying
     VARIABLEDATE
If today    is the twelfth,   we now say
     12 DATE !

that is, we put a twelve on the stack, then give the name of the
variable,   then finally  execute the word [], which is pronounced
store.    This phrase stores the number twelve into the variable
DATE.
Conversely,    we can say




t For Beg inners
Suppose your computer generates        bank statements    all day, and
every statement    must show the date.     You don't want to keep the
date on the stack all the time, and you don't want the date to be
part of a definition    that you'd have to redefine    every day. You
want to use a variable.

                                    183
184                                                                                Starting          FORTH




         DATE@

that  is, we can name the variable,      then execute    the word [fil,
which is pronounced   fetch.   This phrase   fetches  the twelve  and
puts it on the stack.  Thus the phrase

         DATE @ • 12 ok

prints     the    date.

To make          matters       even     easier,        there       is   a FORTH word                 whose
definition        is this:

         : ?      @ •

So instead         of "DATE-fetch-dot,"              we could       simply       type

         DATE ? 12 ok

The value of DATE will be twelve                        until      we change        it.       To change
it, we simply store a new number:

         13 DATE ! ok
         DATE? 13ok

Conceivably             we could      define      additional         variables          for    the   month
and year:

         VARIABLE DATE VARIABLE MONTH VARIABLE YEAR

then     define     a word called          !DATE (for          "store-the-date")              like   this:

         : !DATE          YEAR !      DATE I      MONTH ! ;

to be used like            this:

         7 31 80 !DATE ok

then     define     a word called          .DATE (for          "print-the-date")              like   this:

         : .DATE          MONTH ?      DATE ?       YEAR ? ;

Your FORTH system already    has a number of variables   defined; one
is called   !BASE!. !BASE! contains    the number base th~ou're
currently   wor~in.        In fact,  the definitions     of ~ and
!DECIMAL! (and ~.      if your system has it) are simply

          DECIMAL 10 BASE •I               •
                                           I
          HEX 16 BASE ! ;
          OCTAL 8 BASE ! i
8 VARIABLES,   CONSTANTS, AND ARRAYS                              185




You can work in any number base by simply storing    it into IBASEl.t
Somewhere in the definitions    of the system words which perform
input and output number conversions,  you will find the phrase
     BASE @
because the current value of J-g-As~lis used in the conversion
process.   Thus a single routine can convert numbers in ~ base.
This leads us to make a formal statement       about the use of
variables:




A Closer   Look at Variables

When you create   a variable   such as DATEby using the phrase
     VARIABLEDATE
you are really   compiling   a new word, called      DATE, into   the
dictionary.  A simplified view would look like this:




tFor Experts
A three-letter    code such as an airport   terminal name, can be
stored    as a single-length  unsigned    number in base 36. For
example:
     : ALPHA 36 BASE       ; ok
     ALPHAok
     ZAP U~P   ok
186                                                            Starting     FORTH




                                                    t
                                     DATE

                                instruction code
                                 appropr iate for
                                    variables

                                  space for the
                                  actual value
                                  to be stored



DATE is like any other word in your dictionary       except  that you
defined  it with the word !VARIABLE! instead  of the word I]. As a
result, you didn't  have to define  what your definition    would do;
the word jVARIABLEj itself  spells out what is supposed to happen.
And here is what happens:

When you say

      12 DATE !




Twelve goes     onto     then the text                  and, finding  it,
the stack,               interpreter   looks            points it out
                         up DATE in the                 to !EXECUTEl.
                         dictionary




t For Experts
In the next chapter   we'll   show you what a dict i onary          entry   really
looks like in memory.
8 VARIABLES, CONSTANTS, AND ARRAYS                                   187




       DATE
      code for
      variables
       empty
         cell     2076




!EXECUTE! executes     a variable   by copying    the address  of the
variable's "empty"   cell (where the value will   go) onto the stack.t




The word I] takes the ad-               value into that location.
dress (on top) and the value            Whatever number used to be
(underneath),  and stores the           at that address   is replaced
                                        by the new number.



(To remember what order the arguments belong in,       think of setting
down your parcel, then sticking the address label      on top.)




tFor Beginners

In computer terminology,    an address   is a number which identifies
a location   in computer    memory.    For example,    at address    2076
(addresses   are usually    expressed     as hexadecimal,     unsigned
numbers),  we can have a 16-bit representation        of the value 12.
Here 2076 is the "address";   12 is the "contents."
188                                                   Starting   FORTH




The word tfilexpects one argument only:   an address,    which in this
case is supplied by the name of the variable,  as in
        DATE@




                                       DAT£

                                        2. 2076

Using the value on the stack as an address,      the word [IDpushes
the contents    of that location   onto the stack,   "dropping"  the
address.   (The contents of the location  remain intact.)



Using a Variable        as a Counter

In FORTH, a variable
is ideal for keeping
a count of something.
To reuse     our egg-
packer    example,   we
might keep track      of
how many eggs        go
down the conveyor
belt in a single day.
(This   example    will
work at your terminal,
so enter it as we go.)
First   we can define
        VARIABLE EGGS

to keep the count in. To start with a clean slate       every morning,
we would store    a zero into EGGS by executing          a word whose
definition looks like this:
        : RESET   0 EGGS •I I•
Then somewhere in our egg-packing   application,     we would define a
word which executes   the following     phrase     every time an egg
8 VARIABLES, CONSTANTS, AND ARRAYS                                                                    189




passes      an electric         eye on the        conveyor:

         1 EGGS +!

The word [Il adds the given                      value to the contents                  of the     given
address. t {It doesn't bother                     to tell you what the                contents      are.)
Thus the phrase

         1 EGGS +!

increments              the    count    of eggs   by one.      For                    purposes      of
illustration,          let's   put this phrase  inside a definition                      like this:

         : EGG         1 EGGS +! 1

At the      end of the         day,    we would say

         EGGS?

to find         out how many eggs went             by since        morning.

Let's     try    it:

         RESET ok
         EGG o-k-
         EGG ok
         EGG ok
         EGGS? 3 ok

Here's     a review        of the words we've            covered      in the        chapter      so far:




tFor     the     Curious

l+"'ilis usually        defined            in assembly     language,          but    an equivalent
fiigh-level        definition         is

         : +!      DUP @ ROT          + SWAP ! 1
190                                                                          Starting       FORTH




  VARIABLE xxx                                             Creates       a variable
                                                           named xxx;
                            xxx:          -- adr)          the word xxx returns
                                                            its    address       when
                                                           executed.

                            (n adr --         )            Stores  a 16-bit       number
                                                           into the address.

  @                         (adr -- n)                     Replaces       the address
                                                           with its    contents.

  ?                         (adr --       )                Prints the contents     of
                                                           the address,   followed
                                                           by one space.

  +I                        (n adr --         )            Adds a 16-bit        number to
                                                           the    contents        of the
                                                           address.




Constants


While    variables       are normally      used for
values that may change,        constants    are used
for values that won't change.           In FORTH, we                              LIMIT
create   a constari"tand     set its value at the                            instruction code
same time, like this:                                                         appropriate for
                                                                                 constants
       220 CONSTANT LIMIT

Here we have      defined a cohstant                        named                  220
LIMIT, and given it the value 220.                         Now we
can use the word LIMIT in place                            of the
value, like this:

         : ?TOO.HOT         LIMIT > IF • " DANGER-- REDUCE HEAT " THEN ;

If the number on the stack                    is greater      than    220, then    the     warning
message will be printed.

Notice      that   when we say
       LIMIT

we get      the    value,     not   the       address.      We don't     need     the     "fetch."
8 VARIABLES, CONSTANTS, AND ARRAYS                                                      191




This is an important difference   between variables     and constantsJ
The reason for the difference   is that with variables,     we need the
address    to have the option      of fetching    or storing.       With
constants,   we always want the value; we almost never store.
One use for constants         is to name               a hardware    address.        For
example,   a microprocessor-controlled                   camera application        might
contain  this definition:
         : PHOTOGRAPH SHUTTER OPEN TIME EXPOSE SHUTTER CLOSE ;

Here the word SHUTTER has been defined       as a constant                       so that
execution    of SHUTTER returns     the hardware    address                       of the
camera's shutter.  It might, for example, be defined:

         HEX
         3E27 CONSTANTSHUTTER
         DECIMAL

The words OPEN and CLOSE might               be defined        simply   as

              OPEN     1 SWAP
              CLOSE     O SWAP

so that        the phrase
         SHUTTER OPEN

writes        a "l" to the shutter    address,       causing    the shutter    to open.

Here are         some situations      when    it's     good    to define      numbers     as
constants:


         1.     When it's     important  that you make your application     more
                readable.       One of the elements     of FORTH style   is that
                definitions       should   be self-documenting,       as is the
                definition     of PHOTOGRAPHabove.




t For People          Who Intend   to Use polyFORTH's          Target   CompilerT.M.

In your case the difference    is more profound.   A constant's                     value
will be compiled     into PROM; a variable     compiles   into                    PROMa
reference  to a location   in RAM.
192                                                            Starting      FORTH




       2.   When it's more convenient         to use a name instead      of the
            number.       For example,     if you think      you may have to
            change     the value (because,      for instance,    the hardware
            might get changed)         you will only have to change         the
            value     once--in      the block     where     the constant      is
            defined-then       recompile  your application.
       3.   When you are using the same value many times in your
            application.       In the compiled   form of a definition,
            reference    to a constant requires less memory space.t




  CONSTANTxxx         (n --   )              Creates   a constant           named
                      xxx:    ( -- n)        xxx with the value             n; the
                                             word xxx returns              n when
                                             executed.




tFor   polyFORTH Users

Because of reason 3, polyFORTH includes             constant-definitions             of
two often-used  numbers:

       0 CONSTANT0
       l CONSTANTl
8 VARIABLES, CONSTANTS,ANDARRAYS                                                            193




Double-length        Variables    and Constantst


You can define   a double-length                  variable          by using       the   word
!2VARIABLEj. For example,
     2VARIABLEDATE
Now you can use the FORTH words [Ii] (pronounced        two-store)   and
@ID(two-fetch)    to access this double-length    variable.      You can
store a double-length    number into it by simply saying
     800,000 DATE 2!
and fetch     it back with
     DATE 2@ D. 800000 ok
Or you can store        the full month/date/year             into   it, like this:
     7/16/81 DATE 2!
and fetch     it back with
     DATE 2@ .DATE 7/16/81 ok
assuming that you've         loaded     the version          of .DATE we gave in the
last chapter. t
You can     define    a double-length       constant         by using     the   FORTH word
!2CONSTANT!,like this:
     200,000 2CONSTANTAPPLES
Now the word APPLES will            place    the double-length             number on the
stack.
     APPLES D. 200000 ok




tFORTH-79 Standard
The words described  in this            section        are   not required          except    in
the Double Number Word Set.
tFor polyFORTH Users
polyFORTH uses an even-more-clever                arrangement           to store    the date
as one single-length integer.
194                                                                 Starting    FORTH




Use of !2CONSTANTibecomes necessary           when you need to include   a
double-length   va ue inside    a definition.      In FORTH the only way
to do this is by first     defining     the double-length     value   as a
!2CONSTANT!. For example,     to define     a word which adds 400,000 to
a double-length   value on the stack, we must define
       400,000 2CONSTANTMUCH
       : MUCH-MORE MUCHD+

in order       to be able      to say
       APPLES MUCH-MORED. 600000 ok t

As the prefix    "2" reminds     us, we can also use !2CONSTANT! to
define   a pair of single-length     numbers. The reason for putting
two numbers under the same name is a matter of convenience        and
of saving space in the dictionary.

As an example,        recall     (from Chap. 5) that   we can use the phrase
        355 113 */
to multiply  a number by an a                                        We could    store
these two integers  as a...._ ______ ......,

        355 113 2CONSTANTPI

then    simply     use the phrase

        PI*/
as in

        10000 PI    */ . 31415 ok
Here is a review        of the double-length       data-structure      words:




t For polyFORTH Users
polyFORTH includes             the following  definition    for     a double-length
zero for convenient            use inside a colon definition:
        O. 2CONSTANT0.
8 VARIABLES, CONSTANTS,ANDARRAYS                                                    195




  2VARIABLExxx       ( --                          Creates a double-length
                                                   variable  named xxx;
                     xxx:           -- adr}        the word xxx returns
                                                   its address   when exe-
                                                   cuted.
  2CONSTANTXXX       (d --     )                   Creates a double-length
                                                   constant     named xxx
                                                   with the valued;
                     xxx:      ( -- d)             the word xxx returns
                                                   the valued     when exe-
                                                   cuted.
  21                 (d adr --         )           Stores a double-length
                                                   number   into   the ad-
                                                   dress.
  2@                     (adr -- d}                Returns  the double-
                                                   length contents of the
                                                   address.


Arrays

As you know, the phrase
       VARIABLEDATE
creates   a definition      which conceptually            looks like this:


                                           DATE

                                           code

                                         room fora
                                    single-length value




Now if you say
       2 ALLOT
an additional    two bytes         are allotted     in the definition,       like this:
196                                                                                Starting      FORTH




                              DATE
                              code

                       room for a
                  single-length value
                                                   room for two single length values
               1-- --         --------i            (or one double-length value)
                                               ]
                               ditto



The result    is the same as if ~ou had used l2VARIABLEJ.        By
changing   the argument  to !ALLO'f, however,   you can define 2.!!.Y.
number of variables     under    the same name.    Such a group of
variables  is called an "array."

For example,                 let's  say that in our laboratory,  we have                       not just
one, but five                burners that heat various kinds of liquids.




We can make our word ?TOO-HOT check that all five burners     have
not exceeded   their individual limit if we define LIMIT using an
array rather than a constant.

Let's   give     the array                the name LIMITS, like         this:

        VARIABLE LIMITS                    8 ALLOT

The phrase     8 ALLOT" gives
                        11
                                                     the   array     an extra          eight   bytes   or
four cells (five cells in all).
8 VARIABLES , CONSTANTS, AND ARRAYS                                               197




                           LIMITS
                                              addresses

                           code

                         room for                3162
                      burne r-O's limit
                         room for
                                                 3164
                      burner-1's limit

                         room for
                                                 3166
                      burner-2"s limit
                         room for
                      burner-3's limit           3168

                         room for
                      burner-4's limit          316A




Suppose we want t h e limit for               burner    0 to be 220.   We can   store
this value by simply sayi ng
       220 LIMITS !

because LIMITS r etur ns the address of the first cell in the array.
Suppose we want the limit for burner 1 to be 340. We can store
t h is value by addi ng 2 bytes to the ad dress of the original cell,
like this:
       340 LIMITS   2+ !
                                                                        LIMITS
                                                                        code


 340            LI M ITS          [EJ

                                                                                 31"



                                  ts-
                                    ~
                                          0
198                                                                         Starting       FORTH




We can store         limits    for burners            2, 3, and 4 by adding       the
"offsets"     4, 6, and 8, respectively,                 to the original   address.
Since     the offset      is always  double            the burner   number, we can
define the convenient         word
        : LIMIT      2* LIMITS + ;

to take        a burner number on the stack            and compute           an address      that
reflects        the appropriate offset.t

Now if we want            the     value   170 to be the      limit         for    burner    2, we
simply say

        170 2 LIMIT

or similarly,       we can fetch          the limit   for burner     2 with the phrase

        2 LIMIT?      170 ok

This technique    increases    the usefulness                    of the      word      LIMIT,   so
that we can redefine     ?TOO.HOT as follows:

           ?TOO.HOT ( burner# temp -- )
              LIMIT @ > IF " DANGER-- REDUCE HEAT " THEN

which      works like     this:

        210 0 ?TOO.HOT ok
        230 0 ?TOO.HOT DANGER                 REDUCE HEAT ok
        300 1 ?TOO.HOT ok
        350 1 ?TOO.HOT DANGER                 REDUCE HEAT ok

        etc.




tFor    Beginners

a)      Some people  call the "offset"    an "index,"                       and some people
        say that one uses an offset  to "index into"                       an array.

b)      The reason    we number our burners  O through                           4 instead  of 1
        through   5 is so that  we can use the burner                             number itself
        (doubled for byte addressing)  as the offset.
        A thing which most people wouid call the "first"      in a series,
        programmers   think of as the "zeroth.    Still,   if you need to
                                                            11


        call   the burner   on the left   "burner  1,    you can simply
                                                                      11


        change LIMIT to say
                : LIMIT         1- 2* LIMITS+;
8 VARIABLES, CONSTANTS, AND ARRAYS                                               199




Another    Example       Using     an Array       for   Counting


Meanwhile,    back at the egg ranch:

Here's   another example    of an array.      In this    example,   each
element of the array is used as a separate      counter.     Thus we can
keep track of how many cartons   of "extra large"     eggs the machine
has packed, how many "large,"   and so forth.

Recall from our previous          definition   of EGGSIZE (in Chap. 4) that
we used four categories          of acceptable    eggs, plus two categories
of "bad eggs."

      0 REJECT
      1 SMALL
      2 MEDIUM
      3 LARGE
      4 EXTRA LARGE
      5 ERROR

So let's   create    an array    that       is six cells   long:

      VARIABLE COUNTS 10 ALLOT
The counts will be incremented  using the word [TI), so we must be
able to set all the elements in the array to zero before we begin
counting.  The phrase
      COUNTS 12 0 FILL
                     :

will fill twelve bytes,     starting  at the address    of COUNTS, with
zeros.     If your FORTH system includes      the word lERASEi,t it's
better   to use it in this situation.    IERASEI fills the given number
of bytes with zeroes.     Use it like this:

      COUNTS 12 ERASE


  FILL                 (adr n b --          )       Fills   n bytes     of memory,
                                                    beginning    at   the address,
                                                    with value b.

  ERASE                (adr n --        )           Fills   n bytes     of memory,
                                                    beginning    at   the address,
                                                    with zeroes.




t FORTH-79 Standard

!ERASE! is included      in the optional          Reference    Word Set.
200                                                                              Starting         FORTH




For convenience,         we can put the              phrase       inside    a definition,           like
this:

        : RESET     COUNTS 12 ERASE ;

Now let's  define    a word which will give us the address of one of
the counters,     depending  on the category   number it is given  (0
through 5), like this:

        : COUNTER     2*    COUNTS + ;

and another   word which            will         add one to the        counter      whose         number
is given, like this:

        : TALLY     COUNTER 1 SWAP +! ;

The "l" serves   as the increment                          for [8], and !SWAP! puts                  the
arguments for [BJ in the order they                       belong,  i.e., (n adr -- ).
Now, for instance,         the phrase

        3 TALLY

will    increment   the counter            that     corresponds       to large       eggs.

Now let's  define  a word which                   converts    the     weight      per dozen         into
a category   number:
          : CATEGORY         DUP 18          < If     0   ELSE
                             DUP 21          < If     1   ELSE
                             PUP"    Z4      (    IF Z ELSE
                             DUP 27          < IF 3 ELSE
                             DUP 30          < IF 4 · ELSE
                                                      5
                         THEN THEN THEN THEN THEN                          SWAP DROP         ;t



(By the time we get to the phrase    "SWAP DROP," we will have two
values on the stack:    the weight which we have been !DUP!ing and
the category    number, which will be on top.    We want only the
category   number; "SWAP DROP" eliminates the weight.)




t For Experts
We'll    see a simpler      definition            at the end of this           chapter.
8 VARIABLES, CONSTANTS, AND ARRAYS                                                201




For instance,      the phrase

       25 CATEGORY

will leave  the number 3 on the stack.    The above definition          of
CATEGORY resembles    our old definition   of EGGSIZE, but, in the
true FORTH style of keeping   words as short as possible,        we have
removed the output messages from the definition.        Instead,    we '11
define  an additional  word which expects    a category      number and
prints an output message, like this:

        : LABEL      DUP 0: If    " REJECT
                                                      ..
                                                     ..
                                                   ELSE
                                                   ELSE
                     DUP 1 = If
                     DUP 2 = If        ..
                                  " SMALL
                                    MEDIUM "       ELSE
                                  " LARGE "        ELSE
                     DUP 3 = If
                     DUP 4 = If        ..
                                    EXTRA LARGE " ELSE
                                  " ERROR "
                      THEN THEN THEN THEN THEN DROP ; t
For example:

       1 LABEL SMALL ok

Now we can define       EGGSIZE using        three   of our own words:
       : EGGSIZE      CATEGORY DUP LABEL TALLY ;

Thus the phrase
       23 EGGSIZE

will   print

       MEDIUM ok

at your terminal      and update     the counter          for medium eggs.

How will we read the counters   at the               end of the day?    We could
check each cell in the array separately                with a phrase such as

       3 COUNTER ?

(which would tell us how many "large"      cartons were packed).   But
let's get a little  fancier    and define    our own word to print   a
table of the day's results  in this format:


tFor   Experts

We'll see      a more elegant      version     of this      definition   in the   next
chapter.
202                                                         Starting     FORTH




      QUANTITY             SIZE
            1             REJECT
       112                SMALL
       132                MEDIUM
       143                LARGE
       159                EXTRA LARGE
         0                ERROR

Since we have already   devised category            numbers, we can simply
use a [QQ]loop and index on the category           number, like this:

                REPORT   PAGE   ." QUANTITY    SIZE "            CR CR
                    6 0 DO I COUNTER e 5 U,R
                              7 SPACES I LABEL CR                  LOOP


(The phrase
      I COUNTER@ 5 U.R
takes the category   number given by [!], indexes into the array,
and prints the contents   of the proper element in a five-column
field.)


Factoring        Definitions

This is a good time to talk about factoring               as it applies     to
FORTH definitions  . We've just seen an example          in which factoring
simplified  our problem.
Our first definition     of EGGSIZE, from Chap . 4, categorized    eggs by
weight and printed       the name of the categories      at the terminal.
In our present version we factored        out the "categorizing"   and the
"printing"      into two separate       words.    We can use the word
CATEGORYto provide the argument either for the printing            word or
the counter-tal    l ying word (or both).    And we can use the printing
word, LABEL, in both EGGSIZE and REPORT.
As Charles       Moore, the inventor    of FORTH, has written:
      A good FORTHvocabulary contains a large number of small
      words. It is not enough to break a p r oblem into small
      pieces.  The object is to isolate words that ~ be reused.
For example,        in the recipe :
8 VARIABLES, CONSTANTS, AND ARRAYS                                          203




      Get can of tomato sauce.
      Open can of tomato sauce.
      Pour tomato sauce into pan.
      Get can of mushrooms.
      Open can of mushrooms.
      Pour mushrooms into pan.
you can "factor      out" the getting,   opening,          and pouring, since
they     are common      to both   cans.    Then          you can give     the
factored-out   process a name and simply write:

      TOMATOESADD
      MUSHROOMSADD

and any chef who's graduated  from the          Postfix     School   of Cookery
will know exactly what you mean.

Not only does factoring    make a program easier to write (and fix!),
it saves memory space,     too.   A reusable  word such as ADD gets
defined  only once.     The more complicated    the application,  the
greater the savings.

Here's    another    thought about    FORTH style before     we leave   the egg
ranch.     Recall    our definition   of EGGSIZE
         : EGGSIZE      CATEGORYDUP LABEL TALLY ;

CATEGORY gave us a value which we wanted to pass on to both
LABEL and TALLY, so we include the !DUP!. To make the definition
"cleaner,"   we might have been tempted to take the ,!DUP!out and
put it inside the definition  of LABEL, at the beginning. Thus we
might have written

          EGGSIZE       CATEGORYLABEL TALLY ;

where CATEGORYpasses the value to LABEL, and LABEL passes it on
to TALLY. Certainly this approach  would have worked.  But then,
when we defined REPORT, we would have had to say

      I LABEL DROP

instead     of simply
      I LABEL

FORTH programmers tend to follow this convention:             when possible,
words should    desro~   their     own parameters.        In general,     it's
better  to put the DUP inside the "calling         definition"     (EGGSIZE,
here) than in the "called"     definition  (LABEL, here).
204                                                         Starting   FORTH




 Another      Example -    "Looping"   through   an Array

 We'd like to introduce      a little    technique that is relevant  to
 arrays.    We can best illustrate    this techni~      writing our own
 definition  of a FORTH word called !DUMPj.t ~ is used to print
 out the contents of a series of memory addresses.      The usage is
      adr count DUMP
 For instance,     we could enter
      COUNTS12 DUMP
 to print      out the contents       of our egg-counting     array called
 COUNTS. Since !DUMP!is primarily designed as a programming tool
 to print out the contents        of memory locations,     it prints either
 byte-by-byte        or cell-by-cell,        depending    on the type of
 addressing      the computer uses.      Our version of jDUMPj.will print
 cell-by-cell.
 Obviously our !DUMP!will involve       a @QIloop.   The question  is:
 what should we use for an index?     Although we might use the count
 itself  (0 - 6) as the loop index, it's better to use the address as
 the index.
 The address of COUNTS will be the starting index for the loop,
 while the address plus the count will serve as the limit, like
 this:
        DUMP OVER + SWAP DO CR I @ 5 U.R 2 /LOOP                   t
 The key phrase     here is
      OVER+ SWAP
 which immediately        precedes   the [QQ].




 tFORTH-79 Standard
 The Standard      does not require    jDUMPj.
 tFor Those Whose Systems Do Not Have !/LOOP!
 Substitute     [+LooP).
8 VARIABLES, CONSTANTS, AND ARRAYS                                   205




                   (OVERI                   [E         (SWAP]


                       startin9             endin.9     s-tartinlJ
     count             addrus               oclclrus    address
                                   ......
    startin3            count               startins    er11iin9
    address                                 Clddre~s    addrtss
                       starti~
                       addr•ss
                   I
                       CCc:::=-)


The ending and starting addresses are now on the stack, ready to
serve as the limit and index for the fu2] loop.     Since we are
"indexing  on the addresses,"    once we are inside the loop we
merely have to say
    I@   5 U.R

to print the contents of each element in the array.    Since we are
examining bytes in pairs (because [fil fetches a 16-bit value), we
increment the index by two each time, by using
    2 /LOOP
206                                                                   Starting   FORTH




Byte Arrays


FORTH lets you create    an array in which each element consists    of
a single  byte rather    than a full cell.    This is useful any time
you are storing   a series    of numbers whose range fits into that
which can be expressed     within eight bits.
                     -1.J

                    4$'
                        "'
                    r::'"-I
                   .!f"'
                   l~I~I~ I~ I~ I~I~ I~I
                                       \0




The range of an unsigned   8-bit number is Oto 255. Byte arrays
are also used to store ASCII character    strings. The benefit of
using a byte array instead   of a cell array is that you can get
the same amount of data in half the memory space.
The mechanics  of using       a byte        array   are   the   same as using     a cell
array except that

       1.   you don't have to double the offset,                  since   each   element
            corresponds  to one address, and
       2.   you must use the words @TIand @IDinstead       of ffi and rn].
            These words, which operate      on byte values    only, have
            been given the prefix     "C" because  their typical   use is
            accessing ASCII characters.


  Cl                 (b adr -     )                 Stores       an 8-bit
                                                    value       into   the
                                                    address.

  C@                 (adr -- b)                     Fetches     an 8-bit
                                                    value    'from   the
                                                    address.
8 VARIABLES, CONSTANTS, AND ARRAYS                                                       207




Initializing       an Array


Many situations     call   for an array     whose values   never change
during the operation     of the application     and which may as well be
stored into the array at the same time that the array is created,
just as !CONSTANT!s are.      FORTH provides     the means to accomplish
this through the two words ICREATEI and [J (pronounced         create  and
comma).

Suppose        we want permanent    values     in our LIMITS array.           Instead     of
saying

       VARIABLE LIMITS        8 ALLOT

we can say

      CREATE LIMITS 220 ,          340 ,     170 ,   100 ,   190 ,

Usually the above line         would be loaded            from a disk    block,     but it
also works interactively.

Like the word IVARIABLEI, ICREATEI puts a new name in the
dictionary   at compile  time and returns  the address    of that
definition  when it is executed.   But it does not "allot"    any
bytes for a value.

The word [J takes a number off the stack and stores   it into the
array.  So each time you express  a number and follow it with G],
you add one cell to the array. t


                                                                J'fO    (i]
                                              LIMITS                          LIMITS
                code for-                     code for-                       code for
                C.REATE.                      CREATE                          C.RtATE.

                                               220                            220
               dictionar.Y
                                                                              3'tO


t For Newcomers
Ingrained    habits,  learned           from English   writing,   lead   some
newcomers to forget    to type         the final G]in the line.      Remember
that [J does not separate    the       numbers, it compiles them.
208                                                                   Starting     FORTH




You can access the elements    in a ICREATEI array                 just    as you would
the elements  in a !VARIABLE! array.  For example:

       LIMITS 2+@ 340 ok

You can even store new values    into the array,   just as you would
into a !VARIABLE! array,    as long as you don't       do this in an
application that you someday hope to target    compile.t

To initialize  a byte-array  that has been defined     with !CREATE!,
you can use the word [£J (c-comma). t For instance,    we could store
each of the values used in our egg-sorting  definition   CATEGORYas
follows:

       CREATE SIZES      18 C,    21 C,    24 C,      27 C,   30 C,       255 C,

This would allow us to redefine     CATEGORYusing a [QQ]loop                       rather
than a series of nested [g] ... !THENIstatements, as follows*
        CATEGORY 6 0 DO DUP SIZES I + C@
          < IF DROP I LEAVE THEN LOOP;

Note that we have added a maximum (255) to the                     array    to simplify
our definition regarding category 5.
Including       the initialization    of the SIZES array, this version
takes only      three lines of source text as opposed to six and takes
less space      in the dictionary,  too.




tFor   People    Who Intend    to Use polyFORTH's         Target      Compiler

In a target-compiled   application,  !VARIABLE! arrays will reside in
RAM; tables    defined by !CREATE! and initialized    by G] or ~ will
reside,  fixed, in PROM.

tFORTH-79 Standard

@:Jis included      in the optional       Reference      Word Set.

*For People      Who Don't    Like Guessing     How It Works

The idea here is this:     since there are five possible     catego'ries,
we can use the category       numbers as our loop index.       Each time
around, we compare the number on the stack against          the element
in SIZES, offset     by the current      loop index.    As soon as the
weight on the stack is greater       than one of the elements       in the
array, we leave the loop and use [!] to tell us how many times we
had looped    before  we "left."     Since this number is our offset
into the array, it will also be our category      number.
 8 VARIABLES,    CONSTANTS, AND ARRAYS                                                   209




Here is a list   of the FORTH words we've covered                  in this    chapter:


  CONSTANT xxx      (n --       )                    Creates   a constant        named
                    xxx:        ( --        n)       xxx with the value          n; the
                                                     word xxx returns           n when
                                                     executed.

  VARIABLE xxx      ( --                             Creates    a variable   named
                                                     xxx; the word xxx returns
                    xxx:                -- adr)      its address when executed.

  CREATE XXX        (     --                         Creates   a dictionary    entry
                                                     (head and code pointer
                    xxx:                -- adr)      only) named xxx; the word
                                                     xxx returns   its address when
                                                     executed.

                    (n adr --               )        Stores  a 16-bit     number     into
                                                     the address.

  @                 (adr -- n)                       Replaces    the address     with its
                                                     contents.

  ?                 (adr --             )            Prints   the contents        of the
                                                     address,    followed        by one
                                                     space.
                    (n adr --               )        Adds a 16-bit number to the
                                                     contents of the address.
  ALLOT             (n --       )                    Adds n bytes      to the para-
                                                     meter    field    of the most
                                                     recently   defined word.

                    (n --       )                    Compiles      n into   the next
                                                     available     cell   in the dic-
                                                     tionary.

  C!                (b adr --               )        Stores   an 8-bit       value   into
                                                     the address.

  C@                (adr -- b)                       Fetches   an 8-bit      value       from
                                                     the address.

  FILL                  (adr n b --              )   Fills   n bytes    of      memory,
                                                     beg inning    at the       address,
                                                     with value b.

  BASE                  (n --       )                A variable   which contains
                                                     the value of the number base
                                                     being used by the system.
210                                                                      Starting     FORTH




Double-length      Operators          {Optional     in FORTH-79 Standard)


  2VARIABLE xxx        (    --                       Creates
                                                     variable
                                                              a double-length
                                                              named xxx;
                       xxx:            -- adr)       the word xxx returns                  its
                                                     address when executed.
  2CONSTANTxxx         (d --      )                  Creates   a double-length
                                                     constant    named xxx with
                                                     the value d;
                       xxx:            -- d)         the word xxx returns      the
                                                     valued   when executed.
  2!                   (d adr --                     Stores   a double-length
                                                     number into the address.
  2@                   (adr -         d)             Returns       the double-length
                                                     contents       of the address.


Words Included      in the FORTH-79 Standard              Reference        Word Set

  C,                   (b --      )                  Compiles        b into the next
                                                     available          byte   in the
                                                     dictionary.

  DUMP                 (adr u --                     Displays       u bytes of memory,
                                                     starting       at the address.
  ERASE                (adr n --                     Stores zeroes   into n bytes
                                                     of memory,    beginning    at
                                                     adr,


Additional      Words Available            in Some Systems

  0                         -- 0)                    Returns       the constant     zero.

  1                         -- 1)                    Returns       the constant     one.

  0.                        -- 0 0)                  Returns       the double-length
                                                     constant       zero.



  KEY

  n, nl            16-bit      signed numbe rs             b         8-bit byte
  d, dl, .. .      32-bit      signed numbers              f         Boolean flag
  u, ul, .. .      16-bit      unsigned numbers            c         ASCII character
                                                                     value
  ud, udl,   ...   32-bit      unsigned        numbers     adr       address
8 VARIABLES, CONSTANTS, AND ARRAYS                                   211




Review of Terms

Array             a series   of memory locations    with a single
                  name. Values can be stored and fetched      into
                  the individual  locations by giving the name of
                  the array and adding an offset to its address.
Constant          a value which has a name. The value          is stored
                  in memory and usually never changes.
Factoring         as it applies     to programming      in FORTH,
                  simplifying   a large job by extracting    those
                  elements which might be reused and defining
                  those elements as operations.
Fetch             to retrieve     a value     from   a given    memory
                  location.
Initialize        to give a variable      {or array) ·its initial
                  value{s) before the rest of the program begins.
Offset            a number which can be added to the address of
                  the beginning   of an array to produce    the
                  address  of the desired  location within the
                  array.
Store             to place   a value   in a given memory location.
Variable          a location  in memory which has a name and in
                  which values are frequently stored and fetched.
212                                                     Starting   FORTH




Problems    -   Chapter   8


1.    a) Write two words called      BAKE-PIE and EAT-PIE. The first
         word increases   the number of available    PIES by one. The
         second decreases    the number by one and thanks you for the
         pie.   But if there     are no pies,  it types   II
                                                             What pie? 11
         (Make sure you start out with no pies.)
            EAT-PIE WHATPIE?
            BAKE-PIE ok
            EAT-PIE THANK YOU! ok
      ~    Write a word called     FREEZE-PIES which takes all the
           available  pies and adds them to the number of pies in the
           freezer.  Remember that frozen pies cannot be eaten.
            BAKE-PIE BAKE-PIE FREEZE-PIES ok
            PIES? 0 ok                   --
            FROZEN-PIES?~
2.    Define a word called .BASE which prints the current value of
      the variable   IBASEI in decimal. Test it by first changing
      IBASE! to some value other than ten.    (This one's trickier
      than it may seem.)
            DECIMAL.BASE 10 ok
            HEX .BASE 16 ok
3.    Define a number-formatting      word called   M. which prints   a
      double-length  number with a decimal point.       The position of
      the decimal point within the number is movable and depends
      on the value of a variable    that you will define as PLACES.
      For example, if you store a 11 1 11 into PLACES, you will get
            200,000 M. 20000.0   ok
      that is, with the decimal point one place from the right.         A
      zero in PLACES should produce no decimal point at all.
8 VARIABLES,     CONSTANTS, AND ARRAYS                                   213




4.   In order to keep track of the inventory       of colored pencils
     in your office,  create  an array, each cell of which contains
     the count of a different     colored  pencil.    Define a set of
     words so that, for example, the phrase
          RED PENCILS

     returns  the address  of the cell that contains    the count of
     red pencils,  etc.   Then set these variables   to indicate  the
     following counts:
          23 red pencils
          15 blue pencils
          12 green pencils
           0 orange pencils

5.   A histogram        is a graphic     representation      of a series    of
     values . Each value is shown by the height               or length  of a
     bar.     In this exercise    you will create an array of values and
     print     a histogram     which displays      a line of "*"s for each
     value.       First    create    an array      with about    ten cells.
     Initialize      each element      of the array with a value in the
     range of zero to seventy.            Then define     a word PLOT which
     will print      a line for each value.          On each line print    the
     number of the cell followed by a number of "* "s equal to the
     contents     of that cell.

     For example,    if the array has four cells   and contains           the
     values 1, 2, 3, and 4, then PLOT would produce:

          1 *
          2 **
          3   ***
          4 ****
214                                                            Starting     FORTH




6.    Create an application    that displays  a tic-tac - toe board, so
      that two human player 9 can make their moves by entering      them
      from the keyboard.    For example, the phrase

             4 X!

      puts an "X" in box         4 (counting   starts   with   l) and produces
      this display:
                       I

             X I



      Then the phrase
             3 O!

      puts   an "O" in box 3 and prints        the display:
                           0

             X I



      Use a byte array to remember the contents    of the board, with
      the value l to signify an "X," a -1 to signify   a "O," and a 0
      to signify an empty box.

      (NOTE:        until   we explai11  more about vocabularies,              avoid
      naming        anything    "X," since   this  may conflict           wi th the
      editor's      [ID.)
                                      9    UNDER THE HOOD


Let's stop     for     a chapter          to lift     FORTH's hood   and see what goes
on inside.

Some of the information     contained    herein we've given earlier,
but, at the risk of redundancy,    we're now going to view the FORTH
"machine"  as a whole, to see how it all fits together.



Inside     !INTERPRET!


Back in the first  chapter    we learned   that the text interpreter,
whose name is IINTERPRETI, picks words out of the input stream and
tries to find their definitions     in the dictionary.   If it finds a
word, !INTERPRET! has it executed.




We can perform     these   separate    operations      ourselves      by using
words that perform the component         functions    of !INTERPRET!. For
instance,  the word ~ (an apostrophe,       but pronounced       tick) finds a
definition   in the dictionary     and returns    its address.      If we have
defined GREET as we did in Chap. 1, we can now say

         ' GREET u.        25520 ok

and discover         the    address       of GREET (whatever     it happens   to be).




                                                    215
216                                                                     Starting     FORTH




we may also directly                use !EXECUTEj. !EXECUTE! will execute                       a
definition, given its             address on the stack. Thus we can say
          'GREET EXECUTE HELLO I SPEAK FORTH ok

and accomplish   the same thing                   as if we had merely        said    GREET,
only in a more roundabout way.

If tick cannot  find a word in the                 dictionary,      it executes     IABORT"I
and prints  a question mark.

FORTH's text interpreter     uses a word related    to tick that returns
a zero flag if the word is found.       The name and usa e of the word
varies, t t but the conditional    structure  of the INTERPRET phrase
always looks like this:

          (find   the word)            IF   (convert    to a number)
                                       ELSE (execute    the word)
                                       THEN
      \
that is, if the string   is not a defined   word                    in the dictionary,
 INTERPRET tries   to convert    it as a number.                     If it is a defined
word, INTERPRET executes     it.

The word          ['.] has   several      uses.   For   instance,      you can      use   the
phrase
          I   GREET

to find out whether      GREET has been defined,      without    actually
having to execute     it (it will either print the address or respond
"?").   In systems that only save the first      three characters      of a
name, you can also use the above phrase        to determine    whether     a
name that you want to give to a new definition        will conflict    with
a predefined    name.




tFORTH-79         Standard

The word jFINDI attempts   to find the next word in the input stream
in the dictionary   and then returns   its address or, if not found, a
zero.
!For polyFORTH Users

The word~       attempts    to find the next word in the input stream in
the dictionary.          If the search     is successful,     ~ leaves   the
parameter   field    address    and false;   if unsuccessful,  leaves  IHEREI
and true.
9 UNDER THE HOOD                                                                           217




You can          also use the             address    to iDUMPi the     contents       of the
definition,         like this:
      1
          GREET 12 DUMP

Or you can change     the value of a constant                       by first   finding        its
address, then storing    the new value into it,                   like this:

      110 ' LIMIT

Or you can          use tick to implement   something    called                   "vectored
execution."          Which brings us to the next section   •••



Vectored         Execution


While it sounds hairy,                   the idea of vectored     execution       is really
quite simple.   Instead                  of executing a definition      directly,      as we
did with the phrase

      I   GREET EXECUTE

we can          execute    it indirectly      by keeping   its address                     in a
variable,         then executing    the contents  of the variable, like                  this:
      1
        GREET POINTER !
      POINTER @ EXECUTE

The advantage  is that we can change the pointer    later, so that a
single word can be made to perform different   things at different
times.

Here is an example            that        you can try yourself:


            1 : HELLO           .. ..
                              HELLO" ;
                                                      ..
            2   : GOODBYE            .
                                GOODBYE ;
            3   VARIABLE 'ALOHA
            4     ALOHA    'ALOHA<? EXECUTE
            5
            6
                , HELLO       'ALOHA !


In the first two lines, we've simply created     words which print the
strings   "HELLO" and "GOODBYE."        In line   3, we've defined       a
variable    called    'ALOHA. This will be our pointer.        In line 4,
we've defined      the word ALOHA to execute    the definition      whose
address   is in 'ALOHA. In line 6, we store the address          of HELLO
into 'ALOHA.
Now if we execute            ALOHA, we will         get
218                                                                 Starting     FORTH




       ALOHA HELLO ok

Alternatively,           if we execute       the phrase
       I    GOODBYEI ALOHA I

to store       the address       of GOODBYEinto       'ALOHA, we will   get
       ALOHA GOODBYEok

Thus the same word, ALOHA, can do two different                   things.

Notice    that     we named our pointer       'ALOHA (which      we would
pronounce    tick-aloha).    Since tick provides    an address,   we use it
as a prefix      to suggest   "the address   of" ALOHA. It is a FORTH
naming convention         to use this prefix    for vectored    execution
pointers.

Tick always goes to the next word in the input stream.t     What if
we put tick inside a definition?   When we execute the definition,
tick will find the next word in the input stream,     not the next
word in the definition.   Thus we could define
       : SAY              'ALOHA !

then       enter
       SAY HELLO ok
       ALOHA HELr;o- ok

or

       SAY GOODBYEok
       ALOHA GOODBYEok

to store           the address   of either     HELLO or GOODBYEinto         'ALOHA.

But what if we want tick to use the next word in the definition?+
We must use the word [I'.] (bracket-tick-bracket) instead of tick.+
For example:

            COMING ['] HELLO 'ALOHA
            GOING ['] GOODBYE'ALOHA


tFoRTH-79 Standard

The behavior    of tick   as described                  by the Standard         differs
somewhat from that explained    here.                See Appendix 3.

tFor       Some Small-system,        Non-polyFORTH,       Users

If your keyboard doesn't have a "[" or "]" key, the documentation
that came with your FORTH system should indicate  substitutes.
9 UNDER THE HOOD                                                              219




Now we can say

         COMING ok
         ALOHAHELLO ok
         GOING ok
         ALOHA--m:iODBYE
                       ok

Here's   an example of vectored          execution       that can be found on
certain    FORTH systems.        When FORTH is first          loaded,  the word
!NUMBER! can only convert           single-length          numbers.   But after
double-length        routines     are loaded,         JNUMBERI can convert
double-length     or sin le-length       numbers.      It would not be enough
to simply redefine        NUMBE , because then you would also have to
redefine      INTERPRET and any other             word which uses !NUMBER!.
Instead,   the definition     of JNUMBERjis something like

            NUMBER     'NUMBER @ EXECUTE ;

where J'NUMBERIis the variable            used as a pointer.   When FORTH is
first    loaded,     this   variable        contains  the address       of the
single-length      version.     But when the double-length       routines    are
loaded,     a new definition       called     J(NUMBER)I, with double-length
capability,      is added to the dictionary.         On the line below the
definition     in the load block is the phrase

         ' (NUMBER) 'NUMBER !

When INUMBERIis executed    in the future, whether by !INTERPRET! or
whomever,    the contents     of   NUMBER are fetched       and this
definition  is executed,  giving   NUMBER new-found   double-length
capability.

Here are the commands we've            covered   so far: t

  1
      XXX               ( -   adr)               Attempts    to find   the
                                                  address    of xxx (the
                                                 word that     follows   in
                                                 the input stream) in the
                                                 dictionary.
  [ ']                  compile   time:
                          (   -- )
                        run time:
                           ( -- adr)




t FORTH- 79 Standard

See Appendix      3,
220                                                   Starting   FORTH




The Structure   of a Dictionary         Entry

All definitions,   whether they have been defined    by [;], by
!VARIABLE!,by !CREATE!,or by any other "defining  word," share
these basic parts:
      name field
      link field
      code pointer field
      parameter field
Using the variable       DATE as an example,     here's    how these
components are arranged within each dictionary      entry in systems
that have a three-character-maximum  name field.     In this diagram,
each horizontal line represents one cell in the dictionary:



                     precedence
                     bit
                            \ (previous definition)

                                'I 4          D
                    name
                            l
                         link
                                  A           T

                code pointe r
                  paramete r
                        field




Systems that allow thirty-one-character-maximum        name fields
usually follow the same pattern,      but the name field may take
anywhere from two to thirty-two     bytes, depending  on the name.
The order of the four components may also vary. t




t FORTH-79 Standard
The FORTH-79 Standard allows thirty-one-character-maximum        name
fields,   but does not specify the order of the field within the
dictionary    entry.   The order is considered     implementation-
dependent.
9 UNDERTHE HOOD                                                                    221




In this book, we're only concerned with the functions of the four
components,   not with their   order inside  a dictionary   entry.
We'll use the three-character  version as our example because it's
the simplest.


Name
In our example, the first byte contains      the number of characters
in the full name of the defined       word (there are four letters    in
DATE). The next three bytes contain the ASCII representations         of
the first three letters       in the name of the defined   word. In a
three-character      system, this is all the information  that tick or
bracket-tick-bracket      have to go on in matching up the name of a
definition    with a word in the input stream.
(Notice in the diagram that the sign bit of the "count" byte is
called the "precedence   bit." This bit is used during compilation
to indicate  whether the word is supposed to be executed     during
compilation,  or to simply be compiled into the new definition.
More on this matter in Chap. 11.)


Link
The "link" cell contains           the address of the previous definition
in the dictionary  list.           The link cell is used in searching    the
dictionary.          To simplify   things   a bit,   imagine   that   it   works   this
way:


                      f,i
              UGH
               ME
              CAVE                          Each time the compiler      adds a
              YOU                           new word to the dictionary,      he
                                            sets the link field to point to
              PLOW                          the address    of the previous
          CITY                              definition.   Here he is setting
                                            the link field of CUISINART 'to
         NATION                             point to the definition of CAR.
          CAR
        CUISINART
222                                                              Starting   FORTH




                                                  UGH
                                                  ME
                                                  CAVE
 At search         time,    tick    (or
bracket-tick-bracket,      etc.) starts          YOU
with the most recent          word and           PLOW
follows the "chain"        backwards,
using the address        in each link              CITY
cell to locate       the next defini - +-- -   -N-A_TI_ON_ _   --1
tion back.
                                                  CAR
                                               CUISINART



The link field of the first      definition in the dictionary contains
a zero, which tells   tick       tp give up; the word is not in the
dictionary.


Code pointer
Next is the "code pointer."            The address     contained   in this
pointer     is what distingu i shes a variable     from a constant      or a
colon definition.        It is the address of the instruction       that is
executed first when the particular        type of word is executed.      For
example, in the case of a variable,          the po i nter points to code
that pushes the address of the variable          onto the stack.     In the
case of a constant,        the pointer  points to code that pushes the
contents     of the constant    onto the stack.   In the case of a colon
definition,     the pointer points to code that executes the rest of
the words in the colon definition.
The code that is pointed      to is called   the "run-time code"
because it's used when a word of that type is executed (not when
a word of that type is defined or compiled).
9 UNDERTHE~OOD                                                                223




                                              A
                                                                VARIABLE
      VARIABLEDATE            4     I     D
                                                               run- 1me code
                             A      I     T                    (when executed,
                                  fink                         pushes the
                                                               address of a
                              code pointer
                                                               variable    onto
                                   12                          the stack).




                                              r
    CONSTANT LIMIT            5     I     L                    JCONSTANTI
                              i     I     M                    run-time code
                                                               (when executed,
                                  link
                                                               pushes the
                              code pointer                     contents    of a
                                  220                          constant    onto
                                                               the stack).

              EGGSIZE         7           E
                              G           G




   VARIABLE 'ALOHA            6
                              A           L
                                   link
                              code pointer
                                  2AE4




All variables  have the same code pointer;  all           constants    have    the
same code pointer  of their own, and so on.



Parameter   field

Following   the code pointer      is the parameter      field.    In variables
and constants,      the parameter       field   is only one cell.           In a
l2CONSTANTI or J2VARIABLE], the parameter          field     is two cells.     In
an array,  the parameter    field can be as long as you want it.               In
a colon definition,    the length of the parameter           field depends on
the length     of the definition,        as we'll    explain      in the next
section.

The address     that is supplied   by tick and expected     by IEXECUTEI is
the address     of th~ beginning    of the parameter    field,  called the
parameter-field     address (pfa).
224                                                                                           Starting         FORTH




                                                                            '
                                              count      I       1
                                                2        I       3               head
                                                        link
                                                                            ,
                                                code pointer
                                   pfa O
                                         -           parameter
                                                        field
                                                                       -
                                                                             )
                                                                                 body




By the way, the name and link fields  are often                                         called           the   "head"
of the entry;  the code pointer  and parameter                                          fields           are   called
the "body."



The Basic         Structure          of a Colon           Definition


While the format of the head and code pointer     is the same for all
types of definitions,     the format of the parameter     field varies
from type to type.    Let's look at the parameter    field of a colon
definition.

The parameter              field     of a colon          definition               contains         the     addresses
of    the     previously           defined      words          which        comprise         the    definition.t
Here is the dictionary                       entry      for     the        definition         of PHOTOGRAPH,
which we defined   as:

        : PHOTOGRAPH SHUTTER OPEN TIME EXPOSE SHUTTER CLOSE ;

When PHOTOGRAPHis executed,       the definitions       that are located   at
the successive  addresses     are executed       in turn.     The mechanism
which reads the list of addresses      and executes       the definitions  at
each address is called    the "address    interpreter."




tFor        Experts

The addresses     that comprise                        the body of a colon definition      are
usually code-field     addresses                      (cfa), not parameter-field addresses.
9 UNDER THE HOOD                                                                                        225




                                                p                  The word [iJ.at the end of the
                          10         I                             definition           compiles          the
                          H          I          0                  address        of a word called
                                                                   IEXITI, As you can see in the
                                    link
                                                                   figure,     the address         of IEXITI
                           code pointer                            resides      in the last         cell    of
                                                                   the dictionary            entry.        The
                          adr of SHUTTER
                                                                   address        interpreter            will
                           adr of OPEN                             execute IEXITI when it gets to
 pamm,j                    adr of TIME
                          adr of EXPOSE
                                                                   this
                                                                   executes
                                                                   the
                                                                            address,
                                                                                  the other
                                                                           definition.
                                                                                              just    as it
                                                                                                   words in
                                                                                                     !EXIT!
   field   (                                                       terminates        execution        of the
                          adr of SHUTTER
                                                                   address       interpreter,          as we
                          adr of CLOSE                             will see in the next section.
                            adrof EXIT


Nested     Levels          of Execution


The function       of IEXITI is to return  the flow of execution                                    to the
next     higher-level       definition    that  refers   to the                                   current
definition.       Let's see how this works in simplified   terms.
Suppose        that   DINNER consists                 of   three     courses:

      : DINNER              SOUP ENTREE DESSERT :

and that        tonight's           ENTREE consists            simply      of

      : ENTREE              CHICKEN RICE :


           DINNER               6          J)
                                I          N"
                                    li'nk           We are executing            DINNER and we have
                               code fer       m     just finished
                                                    that       is used
                                                                           the SOUP. The pointer
                                                                                by the      addr~ss
                                o!r'
                                   of
                                 OUP                interpreter         is called   the "interpreter
  Interpreter                   c,dr     of         pointer"       ([!]).    Since the next course
    pointer           b        ENTHE
                                qd,-     •f
                                                     after       SOUP is the           ENTREE,       our
                               DESSERT              interpreter         pointer   is pointing    to the
                                cadr of             cell     that      contains     the address       of
                                ElCIT               ENTREE.
226                                                                     Starting     FORTH




              DINNER



                                      Before we go off and execute ENTREE,
                                      we first   increment the interpreter
                                      pointer  so that when we come back it
                          odr   of
                         ENTREE
                                      will be pointing to DESSERT.
                          adr   af
                         DESSERT




Now we begin      to execute
ENTREE. The first thing we                            DINNER1-------1
 execute      is ENTREE's
"code," i.e., the code that
is pointed to by the "code
field,"   common to all colon                                                        link
definitions.
                                                                                   codefor~
                                                                                     ad,- of
This code does two things:                                      ENTRE'E'           CHICKEN
                                                                                    adt" of
First,  it saves  the con-                                      DESSERT             RICE.
                                                                                    a.Or   of
tents  of the interpreter                                                           EXIT
pointer on the return stack




      DINNER1--------1
                                                          ••. then it puts the
                                     £NTK£F               address      of its own
                                          1-------1
                                                          parameter          field
                                                          address (pfa) into the
                                                          interpreter      pointer.
                                           coJefur§ cf'o. Now the interpreter
                                             Qor of  f pointer        is pointing
                                           CHICKEN po.. to CHICKEN.           So the
                DESSERT                                   address     interpreter
                                                          gets ready to serve
                                                          up the chicken.
9 UNDERTHEHOOD                                                                 227




          DINNER
                            ENTREE                CHICK[N   7     C
                                                            H I
                                                               link
                                                               code
       older
         I                       CHICKE'N                              ,,fQ,

                                  RICE
                                                       1 J
But first, as we did with ENTREE, we increment the pointer so that
when we return it will be pointing to RICE. Then CHICKEN's code
saves this pointer on the return stack and puts CHICKEN'Sown pfa
into the interpreter  pointer.

          PINNER
                     ------1 ENTR££
                                               CHICK
                                                   EN
                     ------1    ---~



                                 RIC£
                                                        ....          ~""



Finally we have our chicken, as the above process conti unes all
down the line to the lowest-level    definition  involved in the
making of the succulent poultry.  Sooner or later we come to the
iEXITJ in CHICKEN.

  DINNER 1-------1
                              ENTR(f                  JE X IT I ta k e s th e
                                                      number off the top of
                                                      the return stack and
                                                      puts it in the inter-
                                                      preter    pointer.     Now
                                                      the address        inter-
                                       CHICk'EN       pre t er continues     with
               DESSE
                  RT                    RICE           the    execution         of
                                                      RICE.
                                       EXIT
228                                                                     Starting       FORTH




      DINNER




                                Eventually,     of course, the IEXITI in
                                ENTREE will put the value on the return
                 DESSERT        stack into the interpreter   pointer.  At
                                last we're ready for DESSERT.
                  EXIT

One Step     Beyond


Perhaps  you're wondering:       what happPns
when we finally     execute      the [EXIT! in
DINNER?   Whose return     address   is on the                                  QUIT
stack?  What do we return to?
Well, remember        that    DINNER has just been                                 l
executed     b EXECUTE, which is a component                                 INTErRET
of INTERPRET.          INTERPRET is a loop which
checks     the entire      input stream.       Assuming
that we entered         Cim:m after     DINNER, then                         EXECUTE
there     is nothin        more to interpret.         So
when we exit
leave
                    INTERPRET, where does that
         us? In the outermost         definition     for                           l
each terminal,      called    jQUITj.                                           DINNER

jQUITI, in simplified      form, looks    like     this:

        : QUIT     BEGIN (clear return stack)     (accept              input)
                    INTERPRET . 11 ok II CR O UNTIL :

(The parenthetical       comments represent     words and hrases not yet
covered.)     We can see that after         the word INTERPRET comes a
dot-quote   message,     "ok," and a @]I, which of course are what we
see after interpretation       has been completed.

Next is the phrase

        0 UNTIL

which    unconditionally    returns       us to the beginning                 of the loop,
where    we clear the return stack        and once again wait                for input.

If    we execute        !QUIT! at   any    level           of   execution,         we will
9 UNDER THE HOOD                                                                        229




immediately     cease   execution       of our application       and re-enter
IQUITl's loop.   The return stack will be cleared          {regardless   of how
many levels     of return     addresses    we had there,      since we could
never use any of them now), and the system will wait for input.
You can see why JQUITJ can be used to keep the message "ok" from
appearing    at our terminal.

The definition             of !ABORT"!uses IQUITI.
                     I
Abandoning          The Nest


It's possible  to skip one level of execution      simply by removing
one return address    from the return stack.    For example,  consider
the three levels of execution    associated  with DINNER, shown here:




    def.
     of
           "
        DINNER                                                                         EX:J


                   SOUP        ENTREE
  DINNER            V
   def.
    of
                                                ~~
                                       CHICKEN        RICE      EXIT
  ENTREE                                    V             V



Now suppose         that     the definition         ENTREE is changed   to:

        : ENTREE           CHICKEN RICE         R> DROP ;

The phrase    "R> DROP" will drop from the rQturn stack the return
address of DESSERT, which was put on just prior to the execution
of ENTREE. If we reload      these definitions  and execute   DINNER,
the IEXITI on the third   level   will take us directly  back to the
first  level.   We'll get SOUP, CHICKEN, and RICE but we'll skip
DESSERT, as you can see here:


    \
  DINNER                                                                      EXIT

                   ~
           SOUP ENTREE                                                  DESSERT EXIT
               V


                            CHICKEN
                                   /'\0./\/\
                                        RICE R>      DROP     EXIT
                               V        V       V     V




                                        •
230                                                                          Starting   FORTH




We're not          necessarily      suggesting     that        you use       "R> DROP" in an
application,         just illustrating      a point.

We've mentioned     that the word !EXIT! removes a return address from
atop the return      stack and puts it into the interpreter             pointer.
The address      interpreter,       which   gets   its bearings        from the
interpreter    pointer,     ,begirs looking    at the next level        up. It's
possible    to include       EXIT in the middle       of a definition.         For
example, if we were to redefine         ENTREE as follows:

        : ENTREE            CHICKEN EXIT      RICE ;

then    when we subsequently                 execute  DINNER, we will exit right
after    CHICKEN and return                to the next course  after the ENTREE,
i.e.,   DESSERT.



      DINNER                                                             EXIT
        '\                                                               /
             '\ ,---...._
             SOUP ENTREE
               V       \.

                            "     /'
                            CtlCKEN
                               V
                                       VRICE       EXIT




This time we get              DESSERT but no RICE.

!EXIT! is commonly used in a disk block to keep the remainder     of
the block from being loaded.   For example, if you edit !EXIT! into
the end of line 5 of a block and load it, any definitions  in line
6 and beyond will not get compiled.



  EXIT                         (   -   )               When compiled             within     a
                                                        colon          definition,
                                                       terminates         execution        of
                                                       that     definition         at that
                                                       point.      When executed        from
                                                       a load      block,      terminates
                                                       interpretation         of the block
                                                       at that point.
  QUIT                         (   - )                 Clears
                                                       returns
                                                                   both
                                                                    control
                                                                           stacks    and
                                                                                  to the
                                                       terminal.        No message     is
                                                       given .
                                                           .
9 UNDERTHEHOOD                                                            231




FORTHGeography

                                   This is a "memory            map 11 t of a
 LOW                               typical    single-user      FORTH system.
MEMORY                             Multiprogrammed         systems    such as
         PRE.COMP1
                 LED               polyFORTH are more complicated,          as
            FORTH                  we will explain      later on. For now
                                   let's take the simple case and ex-
                                   plore each region of the map, one
           ·svSTEM                 at a time.
          VA'RIA8lES

           ELECTIVE
          DEFINITIONS              Precompiled    Portion
                                   In low memory resides           the only
                                   precompiled     portion   of the system
             USER                  (already    compiled into dictionary
          DICTIONARY               form). On some systems this code is
                              -H
                                   kept on disk (often blocks 1 - 8) and
                                   automatically     loaded into low RAM
                                   when you start        up or "boot"   the
                                   computer.      On other    systems   the
                                   precompiled      portion   resides  per-
                                   manently in PROM, where it is active
                                   as soon as you power up the com-
                                   puter.
                                   The precompiled       portion     usually
                                   includes    most of the single-length
                                   math     operators      and     number-
                                   formatting      words , single-length
                                   stack manipulation    operators,    editor
         RETURN STACK              commands, branching      and structure-
              usei
                                   control    words, the assembler,        all
           'IARIAB LES             the defining words we've covered so

            BLOCK
           BUFFERS
 HIGH
MEMORY,___ ____          _,
                                   t For Beg inners
                                   A "memory map" depicts how computer
                                   memory is divided      up for various
                                   purposes   in a particular     system.
                                   Here, low-numbered addresses       begin
                                   at the top ("low memory") and in-
                                   crease as the map goes down. Memory
                                   space is meas~red in groups of 1,024
                                   bytes.   This quantity     is called     a
                                   "K" (from     "kilo-,"     meaning      a
                                   thousand, which is close enough).
232                                                                            Starting   FORTH




far,   and, of course,        the text    and address          interpreters.        t

System     VariabJ,.es
The next section   of memory contains     "system variables"  which are
created  by the precompiled       portion      and used by the entire
system.  They are not generally         used by the user.    l 1NUMBERl,
which we discussed   earlier, is a system variable.


Elective     Definitions

The portion      of the FORTH system that is not precompiled        is kept
on disk in source-text     form. You can elect to load or not to load
any number of these       definitions     to better  control use of your
computer's     memory space.      The load block for all "electives"      is
called    the "electives     block,"   usually  block 9. To compile     the
electives    after you "boot," simply enter
       9 LOAD

(or whichever       block     is the electives         block     for your system).

For example,       in polyFORTH        electives      include  double-     and
mixed-length    operators,   extended      editor   commands, date and time
commands,    and the ability       to add new multiprogrammed            tasks
including    additional     terminals.         You can mask any of these
electives     out of the electives            block    simply by inserting
parentheses.
If your electives          block    contains   this    line:

       ( 32-BIT ARITHMETIC) 30 LOAD                   31 LOAD         32 LOAD

you can avoid       loading        the double-length           routines        by changing   the
line to

       ( 32-BIT ARITHMETIC 30 LOAD                    31 LOAD        32 LOAD)

If you want to change the electives     block after you have already
loaded   it, you must reload  the system (by rebooting)     before  you
can reload    the electives.  (The word !RELOAD), available     on some
systems, will reload the system and not the electives.)




t For Experts
To give   you an idea               of how compact           FORTH can be, all                of
polyFORTH's precompiled              portion resides       in less than 8K bytes.
9 UNDERTHE HOOD                                                             233




User Dictionary
The dictionary will grow into higher memory as you add your own
definitions   within the portion of memory called the "user
dictionary."     The next available      cell in the dictionary   at any
time is pointed to by a variable        called[!!!.  During the process
of compilation,       the pointer   [!!I is adjusted cell-by-cell    (or
byte-by-byte)      as the entry is being added to the dictionary.
Thus [ID is the compiler's    bookmark; it points to the place in the
dictionary    where the compiler can next compile.
[ffi is also used by the word [ALLOTI, which advances               [IDby the
number of bytes       given.   For example,   the phrase
     10 ALLOT
adds ten     to ffi] so that    the compiler      will leave     room in the
dictionary    for a ten-byte     (or five-cell)   array.
A related    word is IHEREI, which is simply defined
     : HERE     H @ ;

to put the value of [ffi on the stack.  The word G} (comma), which
stores a single-length   value into the next available  cell in the
dictionary,  is simply defined
     .,      HERE !     2 ALLOT ;
that is, it stores      a value into lHEREI and advances       the dictionary
pointer two bytes       to leave room for it.
You can use IHEREI to determine how much memory~part  of your
application  requires,  simply by comparing the ~ from before
with the IHERE! after compiling.  For example:
     HERE     220 LOAD HERE SWAP- • 196 ok
indicates  that the definitions    loaded          by block    220 filled   196
bytes of memory space in the dictionary.
234                                                          Starting      FORTH




The Pad
At a certain   distance  from !HERE! in your dictionary,      you will find
a small region     of memory called    the "pad."      Like a scratch  pad,
it is usually used to hold ASCII character        strings   that are being
manipulated   prior to being sent out to a terminal.           For example,
the number-formatting        words use the pad to hold the ASCII
numerals during the conversion      process, prior to !TYPEJ.

The size of the pad is indefinite.        In most systems there    are
hundreds or even thousands  of bytes between the beginning      of the
pad and the top of the parameter   stack.
Since the pad's beginning       address is defined    relative     to the last
dictionar     entry,   it moves every time you add a new definition          or
execute     FORGET or JEMPTYJ. This arrangement                 proves   safe,
however, because the pad is never used when any of these events
are occurring.       The word JPADJreturns    the current      address of the
beginning    of the pad.    It is defined  simply:
       : PAD     HERE 34 +

that is, it returns an address  that is a fixed             number       of bytes
beyond !HERE!. (The actual number may vary.)


Parameter      Stack

Far abovet     the pad in memory is the area reserved        for the
parameter    stack.   Although    we like  to imagine   that  values
actually   move up and down somewhere as we "pop them off" and
"push them on," in reality     nothing  moves.  The only thing that
changes is a pointer  to the "top" of the stack.
As you can    see below, when we "put a number on the stack,"             what
really   happens  is that the pointer       is "decremented"      (so that it
points   to the next location      toward low memory), then our number
is stored    where the pointer       is pointing,     When we "remove        a
number from the stack,"      the number is fetched       from the location
where the pointer     is pointing,     then the pointer     is incremented.
Any numbers above the stack pointer         on our map are meaningless.




tFor   Beginners
"Above" refers         to the higher   memory addresses,   which   are    "lower"
on our map.
9 UNDERTHEHOOD                                                                          235




            empt~   stack                  after ent:erinJ    1        after enterin3   2.
   i
  low
 memo,.:,        18                                JS                          JB
               23't'I                          23'1'1                           2
                Cf87                                1                           J
                             stq ck
 bottom~            0        pointer                0                           0



               GJ                                Gl
                      18                                18
                        2                                2
                                stack
                        1       poi11
                                    t er                 1
                                                                   stack
                        0                                 0        pointer


As new values         are    added     to the       stack,    it    "grows     toward    low
memory."
The stack pointer   is fetched by the word [:ID (pronounced tick-S).
Since ('.m provides   the addre s s of the top stack location,    the
phrase
       'S @

fetches the conten t s of the top of the stack.   This operation,                            of
course, is identical   to that of IDUPJ. If we had five values                               on
the stack, we could copy the fi f th one down with the phrase
       'S 8 +@

(but this     is generally      not considered          good programmi ng practice).
236                                                            Starting   FORTH




The bottom of the stack is pointed     to
by a variable   called  ~ (S-zero).    ~
always contains   the address of the next
                                                                 18
cell below the "empty stack" cell.                                2
For     examplesof good uses of 'S and                            1
illQ], reviewthe definitions  of DEPTH
and of G:filthat we gave in the Handy                             0
Hint at the end of Chap. 3.

Notice that with double-length          numbers,
the high-order       cell     is stored  at the
lower memory address            whether  on the
stack     or in the       dictionary.       The
operators~        and~       keep the order of
cells consistent,     as you can see here.



                                      I        a /2CONSTANT)

                                     low                   N
                                    memory         't
                                                   A M
                                                        link
                                                        code
                                     high          hi9h
                                    rnemor'j
                                                   low
                                       l
Input    Message    Buffer

illQ]also contains  the starting  address   for the "input    message
buffer,"  which grows toward high memory {the same direction         as
the pad).   When you enter text from the terminal,     it gets stored
into this buffer where the text interpreter   will scan it.


Return      Stack

Above the buffer   resides    the return   stack,     which   operates
identically to the parameter     stack.  There are no high-level
FORTH words analogous      to ~ or rn:QJthat    refer    to the return
stack.
9 UNDERTHE HOOD                                                        237




User Variables

The next section     of mem2!.Y contains "user     variables."      These
variables  include !BASE!, l§i, and many others     that we'll   cover in
an upcoming section.

Block Buffers
At the high end of memory reside the block buffers.        Each buffer
provides  1,024 bytes for the contents   of a disk block.     Whenever
you access a block (by listing    or loading     it, for example) the
system copies the block from the disk into the buffer, where it
can be modified    by the editor  or interpreted      by !LOADI. We'll
discuss the block buffers in Chap. 10.

This completes  our journey   across the memory map of a typical
single-user  FORTH system.   Here are the words we've just covered
that relate to memory regions in the FORTH system.t

  H                        adr)        Returns the address     of
                                       the dictionary pointer.
  HERE               ( -- adr)         Returns        the     next
                                       available       dictionary
                                       location.
  PAD                ( -- adr)         Returns the beginning
                                       address      of a scratch
                                       area     used     to hold
                                       character      strings    for
                                       intermediate           pro-
                                       cessing.
  'S                 ( -- adr)         Returns the addr .ess of
                                       the top of the stack
                                       before 'Sis executed.
  so                 ( -adr)           Contains  the address
                                       the bottom    of the
                                       parameter     stack.




tFORTH-79 Standard

!!!I,~, and ~ are not required     by the Standard.
238                                                           Starting       FORTH




The Geography        of a Multi-tasked     FORTH system


  LOW
  MEMORY
              PRE-COMPILED                          USER
                 FORTH                           DICTIONARY

                 SYSTEM
                VARIABLES

                ELECTIVE
               DEFINITIONS

                                                                       User Area-
                                                                       (Terminal task)
              USER AREA 1
              (terminaltask)



              USER AREA 2
              (terminaltask)



               USER AREA 3
               (terminaltask)


              USER AREA 4
               (control task)

                                                               I
                OPERATOR                                           l User Area -
                                                                   ~   (Control task)


                    BLOCK
                                                    USER
  HIGH              BUFFERS                       VARIABLES
  MEMORY
            ~ - - - - - --'

Some FORTH systems (such as polyFORTH) can be multi tasked, t so
that any number of additional tasks can be added. A task may be

tFor   Beg inners

The term "multitasked"           describes a system in which numerous tasks
operate  concurrently           on the same computer without  interference
from one another.
9 UNDERTHE HOOD                                                      239




either a "terminal task," which puts the full interactive   power of
FORTH into the hands of a human at a terminal,        or a "control
task," which controls a hardware device that has no terminal.
Either type of task requires      its own "user area."   The size and
contents    of a user area depends on the type of task, but typical
configurations    for the two types of tasks are shown in the figure.
Each terminal task has its own private dictionary,        pad, parameter
stack, input message buffer,     return stack, and user variables.
This means that any words that you define at your terminal            are
normally not available    to other terminals.     Similarly,   each task
has its owncopies   of the user variables,    such as IBASEI.
Each control    task has a pair of stacks and a small set of user
variables.   Since a control task uses no terminal, it doesn't need
a dictionary    of its own; nor does it need a pad or a message
buffer.
Following     the initial    boot there     is only one tas~, called
jOPERATOij. Loading the electives        block will allocate  space for
the various     terminal  and control-task     partitions.   Thus it is
possible   to reconfigure   the subtasks within a system by altering
the electives     block and reloading    it. But it's beyond the scope
of this book to explain how.
240                                                                Starting     FORTH




User Variables

The following   list shows most of the user variables.     Some we
won't ever mention again.  Don't try to memorize this table.   Just
remember where you can find it.


  so             Pointer to the bottom of the parameter    stack
                 and, for terminal tasks, the start of the input
                 message buffer.
  SCR            For the editor, a pointer to the current                block
                 number (set by LIST and used by L).
  R#             Current character      position      in the editor.
  BASE           Number conversion       base.
  H              Dictionary       pointer.         Pointer    to   the   next
                 available     byte.
  CONTEXT        Contains up to four indexes             for vocabularies
                 to be searched.
  CURRENT        Contains the index of the vocabulary                to which
                 new _definitions will be linked.
  >IN            Pointer      to the current       position   in the     input
                 st r eam.
  BLK            If non-zero,   a pointer  to the block being
                 inte r preted   by LOAD. A zero indicates
                 interpretation    from the terminal   (via the
                 input message buffer).
  OFFSET




User variables   are not like ordinary variables.  With an ordinary
variable   (one defined by the word )VARIABLE!), the value is kept
in the parameter field of the dictionary    entry.
9 UNDERTHEHOOD                                                          241




Each user variable,    on the other hand, is kept in an array cal+ed
the "user table."     The dictionary  entry for each user variable is
located    elsewhere;   it contains  an offset into the user table.
When you execute the name of a user variable,        such as ffil, this
offset is added to the be'ti.nning address of the user table.      This
gives you the address of l!!J in the array, allowing you to use [fil
or m   in the normal way.

                 VARIABLE                 USER           USER Table
                 run-time                 run-time
                 code                     code
                                                     0
      YEAR
       link
       code
       1981
                  j               H
                                  link
                                 code
                                  10
                                           J
                                           ~10
                                                     2
                                                     4
                                                     6
                                                     8
                                                           value of H




The main advantage of user variables    is that any number of tasks
can use the same definition   of a variable    and each get its own
value. Each task that executes
     BASE @
gets the value for BASE from its own user table. This saves a lot
of room in the system while still allowing each task to execute
independently.
User variables   are defined   by the word IUSERI. The sequence of
user variables  in the table   and their offset values vary from one
system to another.
To summarize,     there     are three  kinds of variables:     System
variables  contain values used by the entire FORTH system. User
variables   contain     values that ar,e unique for each task, even
though the definitions        can be used by all tasks in the system.
Regular variables    can be accessible    either system-wide or within
a single task only, depending         upon whether they are defined
within !OPERATOR!   or within a private task.
242                                                                Startin g FORTH




Voe ab ularies

Earli er we menti on ed that the reason the ~ in the editor doesn't
conflict    with the [!] used in a [QQ]loop is that they belong to
separate    "vocabularies."        In a simple FORTH sy s tem there are
thr e e standard     vocabularies:        FORTH, the editor,    and the
asse mbler.
All the words that we've covered           so far bel o ng to the FORTH
vo ca bulary, except for the editor c ommands whi c h bel o ng to the
editor voc abulary.    The ass e mbler vo c a bulary contains   comma nds
that are used to write a ss embly - la ngu age code for your p art icul ar
co mputer.   Since assemb l y co de va r ies from c omputer to c omput e r,
and since asse mbl y-la ng uage p r o gram min g is a whole different
subject, we won't cover it in this book. t
All definitions         are added
to the same dicti on ary in
the order       in which th ey
are co mpiled, regardless
which       vocabulary       they
bel on g to. So vocab ul a r i es
                                 of
                                        QUARTERBACK
                                          COURT
                                          DRIBBLE
                                                      -
                                                          -                r

are not subdivi s io ns of the            INNING
d i ct ionary ; rather t he y ar e
                                          CENTER
independently        linked list s
that weave th r ough it.                 GOALPOST     -~  ~




                                           UMP
For example , in the figure
shown here, there are th ree              STRIKE
vocabularies:           football,
baseball,     and basketball.
All three are c o-resident
                                          CENTER

                                                      --_o
                                                          -
                                          CENTER
in the same d i ctionary,         but
                                         PLACEKICK
when tick         follows        the
basketball         chain,       for     SHORTSTOP
instance,       it only fi n ds
                                           DUNK
words in the basketball
vocabulary.         Even though           HUDDLE          ~




each voca bul ary has a word            FREETHROW
                                                          11
                                                               I
called      CENTER, tick will
find whichever         version     is
                                                                I          I
 ap p r o priate         for    the                       . .;_·
                                                                 --~
                                                              :.;;*~
                                                                        ....
c on text .




tFor the Curious
See Append ix 2.
9 UNDERTHEHOOD                                                                     243




There is another   advantage   besides   exclusivity,    and that is speed
of searches.    If we are talking    about basketball,      why waste time
hunting through the football     and baseball     words?

You can change the context  in which the dictionary is searched
b executing    any of the three  commands !FORTH!, IEDITORI, or
ASSEMBLER. For example, if you enter

     FORTH

you know      for    sure   that   the   search    context        is    the     FORTH
vocabulary.

Ordinarily,     however, the FORTH system automatically                 changes     the
context     for you. Here's a typical scenario:

The system starts        out with FORTH being the context.              Let's say
you start   entering       an application      into a block.    Certain     editor
commands switch the context             to the editor  vocabulary.        You will
stay in the editor        vocabulary     until you load the block and begin
compiling    definitions.        The word [E]will automatically         reset the
context   to what it was before--FORTH.

Different     versions      of FORTH have different  ways of implementing
vocabularies.        Still,    we can make a few general  statements   that
will cover most systems.

The vocabular   to be searched  is specified               by a user variable
called  CONTEXT. As we said, the commands                IFORTHI, IEDITORj, and
ASSEMBLE change the search context.

There is another    kind of vocabulary       "context":    the vocabulary
to which new definitions       will be linked.     The link vocabulary    is
specified  by another    variable   called  ICURRENTI. Because ICURRENTI
normally  specifies    the FORTH vocabulary,          new definitions   are
normally linked to the FORTH vocabulary.

But how does the system   compile   words into the editor      and
assembler vocabularies? By using the word !DEFINITIONS!, as in

     EDITOR DEFINITIONS

We know that the word IEDITORI sets    CONTEXT to "EDITOR."  The
word IDEFINITIONSI · copies whatever is in CONTEXT into ICURRENTj.
The definition of DEFINITIONS is simply

      : DEFINITIONS         CONTEXT @ CURRENT ! ;

Having   entered
     EDITOR DEFINITIONS

any words     that   you compile    henceforth    will   belong        to the   editor
244                                                      Starting   FORTH




vocabulary     until   you enter
      FORTH DEFINITIONS
to reset     !CURRENT!to "FORTH."t
We've presented      this introduction     to vocabularies     mainly to
satisfy     your curiosity,     not to encourage       you to add new
vocabularies     of your own. The problem of defining          different
subsets of application      words with conflicting       names is better
handled by the use of overlays,      which we discussed in Chap. 3.




tFor Curious polyFORTH Users
kolyFORTH allows several vocabularies       to be chained    in sequence.
~ONTEXTJspecifies  the search order.
The polyFORTH dictionary     is comprised   of eight "linked     lists"
which do not correspond with the vocabularies.      At compile time a
hashing function,   based on (usually) the first letter    of the word
being defined,    computes   a "hashing    index."     This index       is
combined with the "current"    vocabulary  to produce an index into
one of the eight lists.
Thus a single list may contain words from many vocabularies,            but
any words with       identical    names belonging         to separate
vocabularies    will be linked to separate   lists.    The distribution
of entries   in each chain is balanced,    and an entire     vocabulary
can be searched by searching    only one-eighth     of the dictionary.
9 UNDER THE HOOD                                                         245




                             A Handy Hint

                How to !LOCATE! a Source      Definition


Some FORTH systems,  such as polyFORTH,          feature   a very   useful
word called !LOCATE!. If you enter
     LOCATE EGGSIZE

FORTH will list       the block that      contains    the definition     of
EGGSIZE.      The only requirements          are that   the word must be
resident   (currently     in the dictionary)      and that the word must
have been loaded         from a block.       You therefore    can locate
system electives      and words in your application,        but you can't
locate   words in the precompiled      portion.
246                                                   Starting   FORTH




  1
      XXX       ( -- adr)       Attempts        to find    the
                                address      of xxx (the word
                                that    follows   in the input
                                stream) in the dictionary.
  INTERPRET     (   -     )     Interprets         the    input
                                stream,    indexed     by   >IN ,
                                until exhausted.

  EXECUTE       (adr --)        Executes      the       dictionary
                                entry     whose         parameter
                                field    address          is on the
                                stack.
  EXIT          (   -- )        When compiled             within     a
                                colon      definition,        termi-
                                nates      execution        of that
                                definition         at that    point.
                                When executed          from ·a load
                                block,      terminates        inter-
                                pretation       of the block at
                                that point.
  QUIT          (   -- )        Clears        both     stacks    and
                                returns         control       to the
                                terminal.          No message      is
                                given.
  HERE                   adr)   Returns the next available
                                dictionary location.
  PAD           ( -- adr)       Returns       the  beginning
                                address     of a scratch      area
                                used    to hold     character
                                strings     for intermediate
                                processing.
  FORTH                         Makes FORTH the              CONTEXT
                                vocabulary.
  EDITOR        (   --    )     Makes           the         editor
                                vocabulary            the    CONTEXT
                                vocabulary.
  ASSEMBLER     (   -     )     Makes
                                vocabulary
                                            the        assembler
                                                      the CONTEXT
                                vocabulary.

  DEFINITIONS   (   -- )        Sets     CURRENT          to    the
                                CONTEXT vocabulary          so that
                                subsequent    definitions        will
                                 be    linked          to     this
                                voe abulary.
9 UNDERTHE HOOD                                                                       247




Common User Variables
(Some not required by the FORTH-79 Standard.)

  so           Pointer to the bottom of the parameter stack and,
               for terminal tasks, the start of the input message
               buffer.
  SCR          For the editor,   a pointer to the current                      block
               number (set by LIST and used by L).
  R#           Current       character     position     in the editor.
  BASE         Number conversion           base.
  H            Dictionary            pointer.          Pointer    to     the   next
               available        byte.
  CONTEXT      Contains up to four indexes               for vocabularies      to be
               searched.
  CURRENT      Contains the index of the vocabulary                    to which new
               definitions will be linked.
  >IN          Pointer        to the      current      position    in the      input
               stream.
  BLK          If non-zero,     a pointer    to the block        being
                interpreted      by LOAD.      A zero     indicates
               interpretation    from the terminal    (via the input
               message buffer).
  OFFSET       Block offset   to disk drives.   The content  of
               OFFSET is added to the stack number by BLOCK.



Additional   Words Available         in Some Systems

  [')              compile        time:             Used only        in a colon
                        -- )
                         (
                   run time:
                                                    definition,
                                                    the      address
                                                                       compiles
                                                                         of the
                         ( -- adr)                  next word in the definition
                                                    as a literal.
  'S               ( -- adr)                        Returns the address of the
                                                    top of the stack before 'S
                                                    is executed.
248                                                            Starting   FORTH




Review of Terms

Address
interpreter           the second of FORTH's two interpreters,         the one
                      which executes    the list of addresses        found in
                      the dictionary     entry of a colon definition.
                      The address     interpreter        also handles     the
                      nesting   of execution      levels    for words within
                      words.
Body                  the code     and parameter      fields       of a FORTH
                      dictionary   entry.
Boot                  simply, to load the pre compiled      portion   of
                      FORTH into the computer so that you can talk to
                      the computer       in FORTH.     This   happens
                      automatically   when you turn the computer on or
                      press "Reset. "
Cfa                   code field address: the address          of a dictionary
                      entry's code pointer field.
Control       task    on a multitasked   system,     a task which cannot
                      converse with a terminal.      Control tasks usually
                      run hardware devices.
Code pointer
field                 the cell in a dictionary      entry which contains
                      the address      of the run - time code for that
                      particular   type of definition.    For example, in
                      a dictionary      entry created    by[;], the field
                      points to the address interpreter.
Defining       word   a FORTH word which creates a dictionar  entry.
                      Examples include G], !CONSTANT!,VARIABLE, etc.
Electives             the set of FORTH definitions       that come with a
                      system but not in the precompiled portion.        The
                      "electives    block"   loads     the blocks     that
                      contain the elective  definitions:     the block can
                      be modified as the user desires.
Head                  the name and link fields     of a FORTH dictionary
                      entry.
Input message
buffer                the region    of memory within a terminal     task
                      that is used to store text as it arrives from a
                      terminal.   Incoming source text is int e rpreted
                      here.
9 UNDERTHE HOOD                                                              249




Link field            the cell in a dictionary    entry which contains
                      the address of the previous definition,      used in
                      searching   the dictionary.     (On systems which
                      use multiple chains, the link field contains the
                      address of the previous definition      in the same
                      chain.)
Name field            the area of a dictionary   entry which contains
                      the name (or abbreviation       thereon  of the
                      defined    word, along    with the number of
                      characters  in the name.
Pad                   the .region of memory within a terminal          task
                      that    is used as a scratch        area   to hold
                      character  strings for intermediate    processing.
Parameter     field   the area of a dictionary    entry which contains
                      the "contents"      of the definition:      for a
                       CONSTANT, the value of the constant;       for a
                       VARIABLE, the value of the variable;        for a
                      colon definition,     the list of addresses     of
                      words that are to be executed in turn when the
                      definition  is executed.   Depending on its use,
                      the length of a parameter field varies.
Pfa                   parameter  field  address;   the address    of the
                      first cell in a dictionary     entry's  parameter
                      field (or, if the parameter     field consists    of
                      only one cell, its address).
Precompiled
portion               the part of the FORTH system which is resident
                      in object form immediately          after the power-up
                      or boot operation.        The precompiled          portion
                      usually includes      the text interpreter         and the
                      address interpreter;      defining,       branching,     and
                      structure-control     words; single-length        math and
                      stack     operators;      single-length           number
                      conversion        and formatting         commands;       the
                      editor; and . the assembler.
Run- time code        a routine,  compiled in memory, which specifies
                      what happens when a member of a given class of
                      words is executed.     The run-time  code for a
                      colon definition    is the address interpreter;
                      the run-time code for a variable      pushes the
                      contents of the variable's  pfa onto the stack.
System variable       one of a set of variables   provided            by FORTH
                      which are referred    to system-wide             (by any
                      task). Contrast with "user variable."
250                                                           Starting   FORTH




Task                in FORTH, a partition       in memory that contains
                    at minimum a parameter       and a return stack and a
                    set of user variables.
Terminal     task   on a multitasked     system,  a task which      can
                    converse    with a human being using a terminal;
                    i.e.,    one which   has a text    interpreter,
                    dictionary,    etc.

User variable       one of a set of variables     provided   by FORTH,
                    whose    values  are unique       for each   task.
                    Contrast with "system variable."

Vectored
execution           the method of specifying         code to be executed
                    by providing     not the address of the code itself
                    but the address       of a location      which contains
                    the address      of the code.         This location     is
                    often called      the "vector."       As circumstances
                    change    within    the system,     the vector    can be
                    reset to point to some other piece of code.
Vocabulary          an independently       linked    subset     of the   FORTH
                    dictionary.
9 UNDERTHE HOOD                                                                251




Problems   -    Chapter    9


1.   First review Chap. 2, Prob. 6. Without changing any of those
     definitions, now write a word called COUNTSwhich will allow
     the judge to optionally     enter the number of counts for any
     crime. For instance,    the entry
           CONVICTED-OF     BOOKMAKING 3 COUNTS TAX-EVASION
           WILL-SERVEm:i!llm17 YEARS ok
     will compute the sentence    for one count            of bookmaking       .and
     three counts of tax evasion.
2.   What is the beginning       address    of your private     dictionary?
3.   In your system,     how far     is the     pad    from the      top   of your
     private dictionary?
4.   Assuming that        DATE has been defined   by !VARIABLE[, what is
     the difference       between these two phrases:
           DATE.
     and
           I   DATE.
     What is the difference       between    these    two phrases:
           BASE.

     and
           I   BASE.

5.   In this exercise   you will create   a "vectored      execution
     array," that is, an array which contains    addresses   of FORTH
     words.  You will also create   an operation    word which will
     execute  one word stored   in the array when the operation
     word is executed.
     Define a one-dimensional     array of two-byte elements which
     will return the nth element's    address when given a preceding
     subscript  n. Define several words which output something at
     your terminal   and take no inputs.      Store the addresses     of
     these output words in various elements of the array.         Store
     the address of a do-nothing     word in any remaining   elements
252                                                Starting   FORTH




      of the array.   Define a word which will take a valid array
      index and execute    the word whose address is stored in the
      referenced  elemen~
      For example,
      1 DO-SOMETHINGHELLO, I SPEAK FORTH. ok
      2 DO- SOMETHING1 2 3 4 5 6 7 8 9 10 ok
      3 DO-SOMETHING
      **********
      **********
      **********
      **********
      **********
      4 DO-SOMETHINGok
      5 DO-SOMETHINGok
                               10   I/O AND YOU


In this     chapter      we'll explain   how FORTH handles      r;ot   of
character    strings   to and from the block buffers and the terminal.

Specifically,      we '11 discuss disk-access     commands, output commands,
string-manipulation         commands, input     commands, and number-input
conversion.



Block   Buffer   Basics


The FORTH system is designed     so that you don't           usually  need   to
think about the mechanics    of the block buffers.              But sooner   or
later you will, so here's how it works.

As we mentioned    earlier,   each buffer is large enough to hold the
contents    of one block     (1024 bytes)     in RAM so that     it can be
edited,  loaded,  or generally    accessed      in any way. While we can
imagine that we're communicating       directly    to the disk, in reality,
the system brings the data from the disk into the buffer where we
can read it.     We can also write        data to the buffer,       and the
system will send it along to the disk.




tFor Beginners

I/O is an abbreviation       for "input-output,"       which refers  to data,
text, or signals   that are sent or received           by the computer.     I/O
devices  include    terminals,    printers,     disk   drives,  push buttons,
etc.


                                       253
254                                                        Starting       FORTH




This arrangement   is called  "virtual memory" because                the   mass
storage memory is made to act like computer memory.
Many FORTH systems use as few as two block buffers, even when the
system is multiprogrammed.  Let's see how this is possible.


  2.0 0 1LIS,:__]             201 ILIST I             202 I LIST !
                   Buffer
           Block                         Block
                      1
           200                          200
                                        :BI ock                  Block.
                      2
                                         201                     201

Suppose there are         two buffers   in your system.    Now imagine       the
following scenario:
First you list block 200. The system reads the disk and transfers
the block to buffer 1, from which jLIST) displays it.
Now you list block 201.        The system copies   block   201 from the disk
into the other buffer.
Now you list block 202. The system copies block 202 from the disk
into the less-recently used buffer, namely buffer 1.
What happened      to the former contents    of buffer l? They were
simply overwritten    (erased) by the new contents.    This is no loss
because  block 200 is still     on the disk.    But what if you had
edited block 200? Would your changes be lost?         No. Here's what
would happen when you listed block 202:
10 I/0   AND YOU                                                            255




         202 ILISTI
                 (a)
           ~              .Block                              .Block

         Di,) 201         200
                          Block
                                                              202
                                                             Block
                                                              201

First the modified  contents  of block 200 would be sent to the disk
to update the former contents    of 200 there,  then the contents  of
202 would be brought into the buffer.          --

The magic word is !UPDATE!, which sets a flag that indicates                 that
the contents       of the most recently      accessed     buffer should be sent
back to disk, rather       than erased,    the next time that the buffer is
needed.       All editor     commands     that change        the contents    of a
block,     whether    adding    or deleting,      include      !UPDATE! in their
definitions.

Every time you or the system try to access            a block, the system
first checks whether     the block is already      in a buffer.      If it is,
fine.    If not, then the system finds      the earliest     buffer    to have
been    accessed.     If the contents       of this    buffer     have been
lUPDATEid, the system copies        the contents    back onto disk, then
finally    copies the newly-accessed    block into the buffer.

This arrangement  lets you modify the contents   of the block any
number of times without    activating  the disk drive   each time.
Since conversing  with the disk takes longer than conversing   with
RAM, this can save a lot of time.

On the other     hand, when there     are several users on a single
system, this arrangement    allows all of them to get by with as few
as two buffers    (2K of memory), even though each may be accessing
a different   block.

Some FORTH systems give their owners the option   to have               as many
block buffers  as they like, depending  on the memory size              and the
frequency  of disk transfers in their own setups.

The word !FLUSHjt forces      all   updated   buffers   to be written    to disk



tFORTH-79 Standard
The Standard's     name for   [FLUSH!
                                    is !SAVE-BUFFERS!.
256                                                                     Starting   FORTH




immediately.       Now that you know about                the buffers,     you can see
why we need IF LUSH!: merely       updating                a buffer    doesn't   get it
written   to disk.

You should also know that when you jFLUSHI, the system "forgets"
that it has your block in a buffer and clears  the buffer's update
flag.   If you list or load the block again,  FORTH will have to
read it from the disk again.

The effective    opposite   of !FLUSHJ is JEMPTY-BUFFERS!, which also
makes the system "forget"      any block it has and clears      any update
flags.     IEMPTY-BUFFERSI      is useful   if you've    ace idently      got
"garbage"t    in a buffer  (e.g., you've deleted     some important     lines
and forgotten    what you had originally,      or generally     messed up)
and you don't want it to get forced onto the disk.           When you list
your block again,    after entering    !EMPTY-BUFFERS!, the system won't
know it ever had your block in memory and will bring               it in off
the disk anew. t

Each buffer has an associated        cell in memory called      the "buffer
status   cell."    It contains   the number of the block       (e.g., 180).t
The system uses it to tell whether       a requested block is already       in
memory.       When you !COPY! a block,     all you are really       doing   is
changing      the number of the block in the buffer      status     cell  and
updating     the buffer.   When it's time for the buffer     to be written
to disk, it will be written    to the new block.

The basic word that           brings   a block in from the disk,              after  first
finding  an available           buffer  and storing  its contents              on disk if
necessary,      is JBLOCKJ.    For   instance,      if   you   say

      205 BLOCK

!he syjtem will copy block 205 from disk into one of the buffers.
 BLOCK also leaves  on the stack the address  of the beginning    of
the buffer that it used.  We'll learn how to use this address  in a
few sections.


t For Beg inners

"Garbage"          is computer        jargon   for data   which   is wrong,
meaningless,       or irrelevant     for the use to which it is being put.

t For Those     Using   a Multiprogrammed          System

Careful!       JEMPTY-BUFFERS! empties           everyone's      buffers.

*For the Curious
The sign bit of the buffer     status cell                     serves   as the "update
fla~     If the number in the buffer status                     cell tests   as negative
by ~,   then the buffer has been "updated."
10 I/0 AND YOU                                                           257




If your application   requires  writing a lot of data to the disk
without reading what's on the disk already    (e.g., to initialize a
disk, write raw data, transfer tape to disk, etc.), then you'll want
to use !BUFFER!.
!BUFFER! is used by BLOCK to assign a block number to the next
available  buffer.  BUFFE doesn't read the contents    of the disk
into the buffer.   Also, BUFFER doesn't check to see whether the
block number has already been assigned to a buffer, so you have
to make sure that no two buffers get assigned to the same number.

  UPDATE          (   --   )          Marks the most recently
                                       referenced       block     as
                                      modified.     The block will
                                      later     be automatically
                                      transferred   to mass storage
                                      if its buffer is needed to
                                      store a different     block or
                                      if FLUSH is executed.
  EMPTY-BUFFERS ( --       )          Marks all block buffers as
                                      empty without necessarily
                                      affecting    their  actual
                                      contents.   Updated blocks
                                      are not written    to mass
                                      storage.
  BLOCK           (u -- adr)          Leaves     the   address      of the
                                      first    byte    in   block   u.   If
                                      the block is not already in
                                      memory, it is transferred
                                      from mass storage            into
                                      whichever       memory buffer
                                      has been least        recently
                                       accessed.       If the block
                                      occupying     that buffer has
                                       been      updated        (i.e.,
                                      modified),     it is rewritten
                                      onto mass storage         before
                                      block u is read into the
                                      buffer.
  BUFFER          (u -- adr)          Obtains   the next      block
                                      buffer,  assigning       it to
                                      block u. The block is not
                                      read from mass storage.
258                                                                   Starting      FORTH




Output Operators

The word IEMITI takes a single ASCII representation   on the stack,
using the low-order   byte only, and prints the character   at your
terminal.  For example, in decimal:
      65 EMIT Aok
      66 EMIT Bok
The word ITYPEI prints     an entire   string of characters at your
terminal,  given the starting   address of the string in memory and
the count, in this form:
       (adr u --        )
We've already    seen ITYPEI in our number-formatting definitions
without worrying about the address and count, because they are
automatically  supplied by [g.
Let's give ITYPEI an address that we know contains     a character
string.  Remember that the starting   address of the input message
buffer is kept by the user variable[§]}?      Suppose we enter the
following command:
      SO@ 12 TYPE
This will type              twelve characters   from the      input   message       buffer,
which contains              the command we just entered:
      SO@ 12 TYPECIII!l:lmSO@
                            12 TYPEok

Let's digress       for a moment to look at the operation          of ~-     At
compile      time, when the compiler         encounters     a dot-quote,     it
compiles         the ensuing    string    right    into   the dictionary,
letter-by-letter,       up to the delimiting       double-quote.      To keep
track of things, it also compiles the count of characters             into the
dictionary      entry.  Given the definiti~
       : TEST      •   II   SAMPLE      II    ;



and looking at bytes in the dictionary   horizontally                      rather      than
vertically, here is what the compiler has compiled:
                                             pfa
                                colon
      4 T E S link              code              ."7SAMPLE              EXI

                                        address
                                                   tof
                                        run• timt c.ode.
                                             for G:::J
10 1/0 AND YOU                                                                      259




If we wanted     to,           we could type the word        "SAMPLE"       ourselves
(without executing             TEST) with the phrase
        1
            TEST 3 + 7 TYPE

where
        ' TEST

gives       us the pfa of TEST,
        3 +

offsets   us past the address             and the   count,   to the   beginning         of
the string   (the letter "S"),           and

        7 TYPE
types       the string     "SAMPLE."

That little        exercise       may not seem too useful.     But let's     go a step
further.

Remember how we defined       LABEL in our egg-sizing          application,
using nested ~ ... jTHENI statements?      We can rework our definition
using ITYPEI. First let's make all the labels        the same length        and
"string  them together"     within    a single  definition       as a string
array.   (We can abbreviate      the longest   label     to "XTRA t.RG" so
that we can make each label         eight characters       long, including
trailing  spaces. -)
            "LABEL"
               • " REJECT SMALL          MEDIUM LARGE        XTRA LRGERROR "

Once we enter

        ' "LABEL" 3 +

to get the address    of the start     of the string,  we can type any
particular label by offsetting     into the array.    For example, if we
want label    2, we simply    add sixteen      (2 x 8) to the starting
address and type the eight characters       of the name:
        16 + 8 TYPE

Now let's redefine              LABEL so that it takes a category-number           from
zero through five              and uses it to index into the string array,         like
this:

            LABEL        8 *    ['] "LABEL" 3 +   + 8 TYPE SPACE ;
Recall  that the word er] is just like ~ except  that                      it may only
be used inside  a definition  to compile the address                       of the next
260                                                     Starting   FORTH




word in the definition    {in this case, "LABEL").t    Later, when we
execute LABEL, bracket-tick-bracket     will push the pfa of "LABEL"
onto the stack.   The number three is added, then the string offset
is added to compute the address of the particular     label name that
we want.
 This kind of string  array is sometimes called a "superstring."       As
 a naming convention,      the name of the superstring    usually     has
.quotes around it.

Our new version  of LABEL will run a little  faster because it does
not have to perform a series   of comparison    tests   before   it hits
upon the number that matches the argument.       Instead    it uses the
argument to compute the address of the appropriate        string   to be
typed.

Notice,  though, that if the argument to LABEL exceeds     the range
zero through     five, you'll   be typing  garbage. If LABEL is only
going to be used within EGGSIZE in the application,       there's  no
problem.    But if an "end user," meaning a person, is going to use
it, you'd better     "clip" the index, like this:
      : LABEL    O MAX 5 MIN LABEL :



  TYPE               {adr u -   )       Transmits     u characters,
                                        beg inning    at address,    to
                                        the current   output device.




tFORTH-79 Standard

See Appendix    3.
10 I/O AND YOU                                                                        261




Outputting     Strings       from Disk


We mentioned    before    that the word IBLOCKI copies    a given block
into an available     buffer and leaves    the address of the buffer on
the stack.   Using this address      as a starting-point,  we can index
into one of the buffer's      1,024 bytes and type any string    we care
to. For example, to print line .0 of block 214, we could say

CR 214 BLOCK 64 TYPElilll!JmJ
( THIS IS BLOCK 214)                                                                   ok
To print     line   eight,    we could       add 512 (8 x 64) to the address,         like
this:
     CR 214 BLOCK 512 + 64 TYPE

Before we give a more interesting      example, it's time                 to introduce
two words that are closely  associated     with ITYPEI.


  -TRAILING              (adr ul --                 Eliminates          trailing      not-
                             adr u2)                blanks    from the string        trailing
                                                    that     starts        at the
                                                    address by reducing          the
                                                    count from ul (original
                                                    byte      count)         to   u2
                                                    (shortened      byte count).
                         (adr u --       )          Same as TYPE except            brucket-
                                                    that the output      string     t~re.
                                                    is moved    to the pad
                                                    prior   to output.      Used ·
                                                    in multiprogrammed
                                                    systems      to    output
                                                    strings     from      disk
                                                    blocks.
                                                                              -!1n
                                                                             /~:J

I- TRAILING! can be used immediately     before the ITYPEI command to
adjust the count so that trailing    blanks will not be printed.  For
instance,  inserting it into our first example above would give us
      CR 214 BLOCK 64 -TRAILING TYPEmmJ
      ( THIS IS BLOCK 214) ok



tFORTH-79 Standard

l>TYPEI is not required.
262                                                          Starting     FORTH




The word l>TYPE! is only used on multiprogrammed            systems to print
strings  from disk buffers.      Instead    of typing the string     directly
from the address      given, it first moves the entire       string  into the
pad, then types it from there.          Because all users share the same
buffers,   the system cannot     guarantee     that by the time !TYPE! has
finished    typing,  the buffer will still     contain   the same block.      It
can guarantee,      however,   that the buffer       will contain   the same
block during the move to the pad. t Since each task has its own
pad, !>TYPE! can safely type from there.

The following     example   uses !TYPE!, but you may substitute         !>TYPE! if
need be.



 231 LIST

       0    < BUZZPHRASE GENERATOR--    VER. 1)         EMPTY
        1
       2 181 LOAD ( RANDOMNUMBERS)
       3
        4   BUZZ 232 BLOCK+ 10 CHOOSE 64 * + 20 -TRAILING TYPE
        5   1ADJ   0 BUZZ
        6   2ADJ 20 BUZZ
        7   NOUN 40 BUZZ
        8   PHRASE   1ADJ SPACE 2ADJ SPACE NOUN;
        9   PARAGRAPH
       10       CR • '' BY USING " PHRASE        COORDINATEDWITH "
       11        CR PHRASE       IT IS POSSIBLE f"OR £VEN THE MOST "
       12       CR PHRASE        TO FUNCTION AS"
       13       CR PHRASE        WITHIN THE: CONSTRAINTS OF"
       14       CR PHRASE         " ;
       15 PARAGRAPH




                                                        (continued)




tFor   Experts

In a multiprogrammed   system, a task only releases   control   of the
CPU to the next task during      I/0 or upon explicit      command,   a
command which is deliberately     left out of the definition    of the
word which moves strings.
10 I/0 AND YOU                                                         263




232   LIST

       0 INTEGRATED           MANAGEMENT             CRITERIA
       1 TOTAL                ORGANIZATION           F"LEXIBILITY
       2 SYSTEMATIZED         MONITORED              CAPABILITY
       3 PARALLEL             RECIPROCAL             MOBILITY
       4 FUNCTIONAL           DIGITAL                PROGRAMMING
       5 RESPONSIVE           LOGJSTICAL             CONCEPTS
       6 OPTIMAL              TRANSITIONAL           TIME PHASING
       7 SYNCHRONIZED         INCREMENTAL            PROJECTIONS
       8 COMPATIBLE           THIRD GENERATION       HARDWARE
       9 QUALIF"IED           POLICY                 THROUGH-PUT
      10   PARTIAL            DECISION               ENGINEERING
      11
      12
      13
      14
      15


Upon loading  the application    block (in this case block 231), we
get something   like the following    output,  although some of the
words will be different  every time we execute PARAGRAPH.


BY USING INTEGRATED POLICY THROUGH-PUT COORDINATED WITH
COMPATIBLE ORGANIZATION CAPABILITY IT IS POSSIBLE FOR EVEN THE MOST
OPTIMAL THIRD GENERATION PROGRAMMINGTO FUNCTION AS
SYSTEMATIZED MONITORED CRITERIA WITHIN THE CONSTRAINTS Or
RESPONSIVE POLICY ~ARDWARE.




As ;lQ.,Ucan    see, the definition     of PARAGRAPH consists of a series
of h..:Jstrings     interspersed    with the word PHRASE. If we execute
PHRASE alone, we get

      PHRASE SYSTEMATIZED MANAGEMENTMOBILITY ok

that is, one word c;:hosen randomly from column 1 in block        232, one
word from column 2 and one from column 3.
                      1
Looking at the definition        of PHRASE, we see that it consists    of
three application       words, lADJ, 2ADJ, and NOUN, each of which in
turn consists     of ':in offset  and the application   word BUZz. The
offset indicates     w~ich column we want to choose a particular     word
from; that    is, th 1 number of bytes     in from the left   margin   of
block 232 that the column beg ins.       The definition  of BUZZ breaks
down as follows:

      232 BLOCK
264                                                        Starting   FORTH




moves block 232 into an available      buffer    and returns    the address
of the buffer's beginning byte.
The word
      +
adds the offset   (0, 20, or 40) to offset      us into   the   appropriate
column in the block.
      10 CHOOSE
returns  a random numbert between       0 and 10 to determine           which
line to take our word from.
      64 * +
multiplies  the random number by 64 (the length of one line) and
adds this number to the buffer      address,  to offset   into the
appropriate   line. The address on the stack is the address of the
word we are going to type.
20 -TRAILING TYPE
adjusts   the maximum count of 20 downwards      so that the count
excludes any trailing blanks after the character    string and types
the string.




tThe random    number generator     is given    in the    following     Handy
 Hint.
10 I/0    AND YOU                                                              265




                                     A Handy Hint
                          A Random Number Generator


This simple randof   number generator     can be useful for games,
although for more sophisticated applications    such as simulations,
better versions are available.

181      LIST
  0 ( RANDOM NUMBER GENERATOR -- HIGH LEVEL)
  1 VARIABLE RND   HERE RND !
  2   RANDOM RND@ 31421 * 6927 + DUP RND
  3:  CHOOSE   < u1 --- u2 l
  4                  RANDOMU* SWAP DROP;
  5
  6        where    CHOOSE returns       a random   integer   within   the   range
  7        0    = or < u2 < u1.      l
  8
  9

Here's how to use it:
To choose a random number between              zero and ten (but exclusive       of
ten) simply enter
         10 CHOOSE
and CHOOSEwill leave          the random number on the stack.
 266                                                            Starting   FORTH




Internal   String    Operators


The commands for moving character       strings             or data arrays    are
very simple.   Each requires  three arguments:              a source address,    a
destination  address, and a count.



                      (adrl   adr2 u --   }   Copies       a reg ion     of
                                              memory u bytes         long,
                                              cell-by-cell     beginning
                                              at adrl,       to memory
                                              beginning     at adr2.    The
                                              move begins       with the
                                              contents      of adrl    and
                                              proceeds      toward    high
                                              memory.
  CMOVE               (adrl   adr2 u --   )   Cop i e s a reg ion       of
                                              memory u bytes        long,
                                              byte-by-byte    beginning
                                               at adrl,     to memory
                                              beginning    at adr2.    The
                                              move begins      with the
                                              contents     of adrl    and
                                              proceeds     toward    high
                                              memory.
  <CMOVE              (adrl   adr2 u --   }   Cop i e s a reg ion     of     ba.ck-
                                              me mor y u bytes    long,        c-
                                              beg inning   at adrl,    to   move
                                              memory beginning         at      I
                                              adr2, but starts   at the~~ .
                                              end of the string      and    ~
                                              proceeds    toward    low
                                              memory.                     ,, ·




tFORTH-79 Standard

The Standard's       IMOVE! expects       a cell   count.      !<CMOVE! is not
required.
10 I/O AND YOU                                                                                 267




Notice      that   these   commands follow            certain    conventions         we've     seen
before:

       1.      When the arguments           include a source and a destination
               (as they     do with        !COPY!), the source   precedes      the
               destination.
       2.      When the arguments   include  an address  and a count                            (as
               they do with !TYPED, the address precedes  the count.


And so with these          three   words the arguments             are
       (source     destination     count    --    )

To move the entire      contents                 of     a buffer     into      the    pad,      for
example, we would write

       210 BLOCK PAD 1024 CMOVE

although  on cell-address            machines         the move might        be made faster
if it were cell-by-cell,           like this:
       210 BLOCK PAD 1024 MOVE

The word I<CMOVE! lets you move a string     to a reg ion                               that     is
higher in memory but that overlaps the source region.t

tFor      beg inners
Let's say that you want to move a string                        one byte to the "right"
in memory (e.g., when you use the editor
character).
                                                                 command    rn
                                                                            to insert   a



   Usin9      l£MOVEl                                                    Usin3 l<CMOVEI

                            If you were to use !CMOVE!,
                            the first        letter     of the
                            string
                            the second
                                      would get copied to
                                              byte,    but that             IHE ILIPI
                            would "clobber"         the second
                            letter     of the string.        The
                            final     result      would    be a
                            string composed of a single                     !HEILILp
                            character.
                            Using     !<CMOVE! in this
                                                                            IH@IL p
                            situation    keeps the string
                            from clobbering        itself
                                                                            IH}HIEIL
                                                                                   p
                            during the move.
268                                                                  Starting     FORTH




To blank an array, we can use the word !FILL!, which we introduced
earlier. For example, to store blanks into 1024 bytes of the pad,
we say
      PAD 1024 32 FILL
Thirty-two       is the ASCII representation        of blank.t


Single -c haracter            Input

The word !KEY!awaits the entry of ·a single key from your terminal
keyboard   and leaves  the character's    ASCII equivalent  on the
stack in the low-order byte.
To execute          it directly,      you must follow      it with    a return,     like
this:
      KEYmI!ilm
The cursor will advance a space, but the terminal will not print
"ok"; it is waiting  for your input.  Press the letter'i'X';"  for
example, and the screen will "echo" the letter   "A," followed by
the "ok." The ASCII value is now on the stack, so enter G}:
      KEY Aok
      .ljjiiil);j/j 65   ok
This saves        you from having        to look in the table        to determine          a
character's       ASCII code.
You can also include IKEYIinside a definition.       Execution of the
definition   will stop, when !KEY! is encountered,      until an input
character   is received.  For example, the following         definition
will list a given number of blocks in series,      starting     with the
current block, and wait for you to press any key before it lists
the next one:
         BLOCKS ( count -- )
           SCR @ + SCR @ DO I LIST KEY DROP LOOP




tFor polyFORTH Users
You may use the word~                   instead,   as in
      PAD 1024 BLANK
10 I/O AND YOU                                                                   269




                               A Handy   Hint

              Two Convenient      Additions     to the   Editor


You might want to make the following               two additions   to your
editor     vocabular  ~ . The use of these          words is a matter   of
preference;      they may or may not already        be included  with your
system.

     EDITOR DEFINITIONS
     : K #I PAD 132 MOVE PAD #F 66 MOVE ;
     : WIPE  SCR @ BLOCK DUP 1024 32 FILL O SWAP                       UPDATE
     FORTH DEFINITIONS

The word K will swap the contents   of the find buffer                 with   that
of the insert buffer. Here's an example of its use:


     AYOU HAVE TH$ RIGHT TO SILENT REMAIN.                                       ok
     ~.llf.11JSILENTamr

     F AIN mI!liID

     YOU HAVE THE RIGHT TO REMAINA.                                              ok
     I                I
     YOU HAVE THE RIGHT TO REMAIN SILENT.                                        ok


Use of @Iput "SILENT" in the find buffer,   and K put it into                  the
insert buffer so that you could insert it where it belongs.

Or if you've just inserted  a string  in the wrong            place,     you can
put the string   into the find buffer   with Kand              then     erase  it
from the line with a simple ~-

The word WIPE blanks the current          block and stores    two nulls in
the first      two character   positions.     (On most systems,    nulls in
the block act just like the word IEXITI, to immediately          terminate
interpretation      of the block, should it be loaded.)
270                                                          Starting    FORTH




In this case we !DROP!the value      left     by [KEY!because        we do not
care what it is.
Or we might add a feature that allows us either            to leave the loop
at any time by pressing     return or to continue            by pressing  any
other    key, such as space.      In this ca~e               will perform   a
conditional   test on the value returned by ~-
         BLOCKS ( count -- )
           SCR @ + SCR @ DO I LIST
               KEY O= ( CR) IF LEAVE THEN LOOP ;
Note that in most FORTH systems,            the   carriage-return        key is
received as a null (zero).

  KEY              (   --   c)              Returns the ASCII value of
                                             the    next     available
                                            character    from the current
                                            input device.


String   Input Commands, from ,the Bottom up

There are several words involved with string input.    We'll start
with the lowest-level of these and proceed to some higher-level
words. Here are the words we'll cover in this section:

  EXPECT           (adr u --     )          Awaits u characters        (or a
                                            carriage    return)    from the
                                            terminal      keyboard      and
                                            stores   them, starting       at
                                            the address.
  WORD             (c -- adr)               Reads one word from the
                                            input     stream,     using     the
                                            character      (usually     blank)
                                            as a delimiter.        Moves the
                                            string      to the      address
                                            (HERE) with the count in
                                            the first byte, leaving the
                                            address on the stack.
  TEXT             (c -      )              Reads a string       from the
                                            input     str earn, using    the
                                            character      as a delimiter,
                                            then sets the pad to blanks
                                            and moves the string to the
                                            pad.
10 I/0   AND YOU                                                            271




The word !EXPECT! stops execution      of the task and waits for input
from your keyboard.     It expects a given number of keystrokes    or a
carriage   return,   whichever    comes first.   The incoming  text is
stored beginning    at the address given as an argument.



                           ~s
                                   T




For example,     the phrase
     SO @ 80 EXPECT t

will await up to eighty         characters   and store    them in the   input
message buffer.
This phrase is the one used in the definition            of JQUITI to get   the
input for !INTERPRET!.
In most systems,    when you press return           or when the limit    is
reached,  !EXPECT! stores a null (zero) into        the string to mark the
end, then allows e 1 ecution to continue.t


t FORTH- 79 Standard
This phrase     is equivalent    to the Standard   word [QUERYJ.
t For Experts
You can use IEXPECTI to accept data from a serial      line, such as a
measuring device.       Since you supply the address and count, such
data can be read directly         into an array.    In a single-user
environment,    you mpy read data into a buffer for storage on disk.
In a multi-user    environment,   however, you must use ~ and later
move the data into the buffer, since another      task may use "your"
buffer.
272                                                       Starting   FORTH




Let's move on to the nex~her-level              string-input     operator.
We've just explained that l2!!!!j contains    the phrase
      • •• SO @ 80 EXPECT INTERPRET
But how does the text interpreter    scan the input message          buffer
and pick out each individual  word there?   With the phrase
      32 WORD
The decimal number 32 is the ASCII representation           for "space."
!WORtj scans the input stream looking for the given delimiter,           in
this case space, and moves the sub-string       into a different   buffer
of its own, with the count in the first            byte of the buffer.
Final!,   it leaves the address of its buffer on the stack, so that
 INTERPRET (or anyone else) knows where to find it.              IWORD!'s
buffer   usually   begins at [ffi, the dictionary      pointer,   so the
address given is !HEREI.




IWORDIlooks for the given                and moves the the sub-string
delimiter in the input                   to !WORDl'sbuffer, with the
message buffer,                          count in the first byte.

When you are executing words directly     from a terminal, !WORD!will
scan the input buffer,  starting    at~-       As it goes along,   it
advances thj inpr buffer pointer,    called !>IN!, so that each time
you execute WORD, you scan the next word in the input stream.
l>INI is a "relative    pointer";   that is, it does not contain    the
actual address but rather       an offset that is to be added to the
actual   address,   which in this case is [[Q]. For example,     after
IWORDIhas scanned the string "STAR," the value of !>INI is five.
                  Input. Messa'le Buffer

!WORD! ignores       initial   occurrences    of the delimiter             (until    any
other character       is encountered).     You could type

       J6j6j6'6j6STAR

(that is, STAR lprecjded by several  spaces) and get                      exactly        the
same string in WORD's buffer as shown above.

When !WORD!moves the sub-string,    it includes                 a blank    at the        end
but does not include it in the count.

We'll get back to !WORD! later     on in this chapter.  For now,
though,   let's look at a word that uses !WORD! and that is more
useful for handling  string input.

iTEXT!,t like iWORDi, takes a delimiter      and scans the input stream
until    it finds   the string  delimited    by it.   It then moves the
string    to the pad.    What is especially    nice about !TEXT! is that
before      it moves the string,     it blanks    the pad for at least
~      - four spaces.    This makes it very convenient       for use with
~-         Here's a simple example:

       CREATE MY-NAME 40 ALLOT
       : I'M 32 TEXT PAD MY-NAME40 CMOVE

In the    first   line we define  an array called   MY-NAME. In the
second    line    we define a word called  I'M which will allow us to
enter
       I'M EDWARDok

tFor   Those Who Don't        Seem to Have jTEXTi

!TEXT! is not required          by the     FORTH-79 Standard.       Its    definition,
however, is
       : TEXT     PAD 7f 32 FILL           WORD COUNT PAD SWAP <CMOVE ;
If you have a polyFORTH system,    the electives     block normally
does not load the block (usually 34) that contains    !TEXT!. In this
case you must add "34 LOAD" to your electives      block and reload
it.
274                                                          Starting     FORTH




The definition       of I'M breaks   down as follows:   the phrase

      32 TEXT

scans the remainder    of the input stream looking  for a space or
for the end of the line, whichever     comes first.  {The delimiter
that we give as an argument to !TEXT! is actuall~d        by !WORD!,
which is included   in the definition  of !TEXT!.) ~ then moves
the phrase to a nice clean "pad."
The phrase

      PAD MY-NAME40 CMOVE

moves forty bytes from the pad into the array              called       MY-NAME,
where it will safely stay for as long as we need           it.

We could     now define    GREET as follows:

      : GREET       • " HELLO, " MY-NAME40 -TRAILING TYPE
                  • II , I SPEAK FORTH. "
so that    by executing    GREET, we get

      GREET HELLO, EDWARD, I SPEAK FORTH. ok

Unfortunately,     our definition of I'M is looking for a space as its
delimiter.     This means that a person named Mary Kay will not get
her full name into MY- NAME.

To get the complete     input stream,         we don't   want to "see"    any
delimiter  at all,  except   the end         of the line.    Instead   of "32
TEXT," we should use the phrase
      l TEXT

ASCII l is a control      character     that  can't    be sent from the
keyboard   and therefore    won't ever appear       in the input buffer.
Thus "l TEXT" is a convention         used to read the entire        input
buffer, up to the carriage    return.   By redefining     I'M in this way,
Mary Kay can get her name into MY-NAME, space and all.
By using other       delimiters,      such as commas, we can "expect"          a
series   of strings    and store each of them into a different           array
for different     purposes.      Consider  this example, in which the word
VITALS uses commas as delimiters          to separate   three input fields:
10 I/0    AND YOU                                                         275




233 LIST

 0 ( ~ORM LOVE LETTER)                EMPTY
 1 VARIABLE NAME 12 ALLOT        VARIABLE EVES 10 ALLOT
 2 VARIABLE l'IE 12 ALLOT
 3 : VITALS     44 TEXT ( , ) PAD :-!AME 14 MOUE
 4              44 TEXT       PAD EVES 12 MOUE
 5               1 TEXT       PAD ME 14 MOVE
 6
 7       LETTER      PAGE
 8            "DEAR"   NAME 14 -TRAILING TYPE
 9        CR " I GO TO HEAVEN WHENEVER-I SEE YOUR DEEP"
10                           EVES 12 -TRAILING TYPE     EVES. CAN "
11        CR "YOU GO TO THE MOVIES ~RIDAV'?"
12                                 CR 30 SPACES   " LOVE,"
13                                 CR 30 SPACES ME 14 -TRAILING TYPE
14        CR " P,S,   WEAR SOMETHING " EVES 12 -TRAILING TYPE
15              TO SHOW O~~ THOSE EVES! " ;


which allows     you to enter

       VITALS ALICE, r LUE,FRED ok

then     enter
       LETTER

It works every      time.
So far all of our input has been "FORTH style";      that is, numbers
precede    commands (so that a command will find its number on the
stack) and strings   follow commands (so that a command will find
its string   in the input stream).    This style makes use of one of
FORTH's unique features:      it awaits your commands; it does not
prompt you.

But if you want to, you may put !EXPECT! inside        a definition     so
that     it wi l l request    input  from you under   control      of the
definition.      For example, we could combine the two words I'M and
GREET into a single        word which "prompts"  users to enter their
names. For example,

       GREET
       WHAT'S YOUR NAME?
at which point      execution   stops   so the user can enter   a name:

       GREET
       WHAT'S YOUR NAME? TRAVIS MC GEE
       HELLO, TRAVIS MC GEE, I SPEAK FORTH. ok
276                                                            Starting   FORTH




We could   do this   as follows:


      : GREET   CR • " WHAT'S YOUR NAME?" so @ 40 EXPECT
                    0 >IN ! l TEXT     CR • " HELLO, 11
                                    11
           PAD 40 -TRAILING TYPE       , I SPEAK FORTH. " :


We've explained      all   the   phrases   in the   above   definition    except
this one:

      0 >IN

Remember that ITEXTI, because           it uses !WORDI, always uses l>INj as
its reference    point.      But when the user enters     the word GREET to
execute    this definition,      the string   "GREET" will be stored in the
in ut message buffer and l>INI will be pointing             beyond  "GREET".
 EXPECT does not use l>IN! as its reference,           so it will store the
user's   name beginning        at ~,     on top of GREET. If you were to
execute     ITEXTI now, it would miss the first        five letters   of the
user's   name.   It'snecessary        to reset l>IN! to zero so that !TEXT!
will look where !EXPEC'Ij has put the name.
10 I/O AND YOU                                                            277




Number Input   Conversions


When you type a number at your terminal,            FORTH automatically
converts  this character      string into a binary value and pushes it
onto the stack.    FORTH also provides        two commands which let you
convert  a character     string     that begins at~      memory location
into a binary value.t

  >BINARY or          (dl adrl -        Converts      the text be-
  CONVERT               d2 adr2)        ginning     at adrl+l      to a
                                        binary     value    with re-
                                        gard to BASE. The new
                                        value    is accumulated
                                        into dl, being left as
                                        d2: adr2 is the address
                                        of the       first      non-
                                        convertible      character.
  NUMBER              (adr -- n or d)   Converts      the text be-
                                        ginning     at adr+l, with
                                        regard     to BASE, to a
                                        binary      value    that      is
                                        single-length           if no
                                        valid    punctuation         oc- ~
                                        curs and double-length              ~
                                        if valid       punctuation         1~
                                        does occur.       The string         .
                                        may contain           a pre-
                                        ceding     negative       sign:
                                         adr    may contain              a
                                        count,     which     will be
                                        ignored.

INUMBERjexists on most systems and is usually        the simpler     to use.
Here's an example that uses !NUMBER]:
     : PLUS    32 WORD NUMBER+ • 11 = 11 •   :



PLUS allows us to prove to any skeptic that       FORTH could      use infix
notation  if it wanted to. We can enter


t FORTH-79 Standard

The Standard   specifies  the name !CONVERT! instead    of J>BINARYj.
In FORTH systems which use three-character    uniqueness,   however,
this choice  conflicts   with the name CONTEXT: hence the name
l>BINARYJ is used instead.       NUMBER is not required       by the
Standard.
278                                                             Starting   FORTH




        2 PLUS 13mi!lmJ = 15 ok

When PLUS is executed,         the     11
                                            2 11 will be on the stack in binary
form, while the "3" will       still        be in the input stream as a string.
The phrase
        32 WORD

reads     the string;    NUMBER converts    it to binary  and puts the
value    on the stack;   + adds the two values; and G1prints the sum.
WUMBERjexpects       on the stack the address of the string that is to
  e converted,     with the count in the first    byte and one trailing
blank, so it's most appropriate      for use after IWORDI. !NUMBER]does
not actually     use the count, however; it only adds one byte to the
address     before    beginning   the conversion.     Thus you can use
iNUMBER!on a string that does not contain         the count in the first
byte, simply by subtracting      one byte from the starting   address of
the string.
i>BINARY! is a more primitive          definition,        being     used in the
definition      of !NUMBER!. You can use !>BINARY! to create                our own
specialized       number input conversion       routines.       Since    >BINARY
returns    the address    of the first   non-convertible         character,     you
can make decisions       based on whether      the character        is a hyphen,
dot, or whatever.         You can also make decisions             based on the
location     of the non-convertible    character     within the number. For
instance,      you can write a routine     that lets you enter a number
with a decimal point in it and then scales it accordingly.
To give a good example of the use of l>BINARYl, Figure 10-1 shows
a definition   of !NUMBER!, This version    reads     any of the
characters

             - • I
as valid     punctuation       characters    which cause the value to be
returned     on the stack as a double-length           integer.  If none of
these characters        appear    in the string,   the value is returned as
single-length.t          This definition      uses the word WITHIN as we
defined    it in the problems for Chap. 4.
Here we use the variable      PUNCT to contain  a flag that indicates
whether punctuation    was encountered.    We suggest that you use an
available user variable    instead.



tFor polyFORTH Users

Your version     of NUMBE behaves similarly   and in addition    leaves
in the user variable       PT  the number of characters      that were
converted    since the last punctuation was encountered.
10 I/0 AND YOU                                                                               279




               FIGURE 10-1.     A DEFINITION               OF NUMBER

 VARIABLE PUNCT                 Creates    a flag that will contain     true
                                if the       number   contains      valid
                                punctuation.
  NUMBER ( adr -      n or d)

   0 PUNCT !                    Initializes             flag:      no punctuation             has
                                occurred.

   DUP l+ C@                    Gets the        first      dig it.
   45 ( -) =                    Is it a minus sign?

   DUP >R                       Saves     the flag          on the return          stack.

   +                            If the first      character    is 11- 11 , adds l
                                (the    flag    itself)     to the address,
                                setting    it to point to the first digit.

   0 0 ROT                      Provides     a double-length                     zero     as an
                                accumulator.

   BEGIN >BINARY                Begins        conversion:             converts      until      an
                                invalid        digit.
   DUP C@                       Fetches       the        invalid      digit.
   32 - WHILE                   While it is not a blank,   checks                           if it
                                is valid punctuation: that is,

   DUP C@ DUP 58 =                a colon,          or
   SWAP 44 48 WITHIN +            a comma, hyphen,                   period,     or slash.
   DUP PUNCT l                  Sets PUNCT to indicate    whether                         valid
                                punctuation has occurred.
   NOT ABORT" ? "               Otherwise        issues         an error       message.

   REPEAT                       Exits    here    if a blank    is detected:
                                otherwise     repeats conversion.

   DROP                         Discards       the address             on the stack.
   R> IF DNEGATETHEN            If the   flag             on the        return      stack      is
                                true, negates             d.
   PUNCT @ NOT IF
     DROP THEN :                If there    was no punctuation,   returns    a
                                single-length       value by dropping     the
                                high-order    cell.
280                                                               Starting     FORTH




A Closer    Look at   (w6iffij

So far we have only talked        about using iWORDi to scan the in~ut
message  buffer     (which holds the characters    that are !EXPECT ed
from the terminal).      But if we recall that the phrase
      32 WORD

is used by the text interpreter,   we realize               that !WORDIactually
scans the input stream,  which is either    the            input message buffer
or a block buffer that is being iLOADied.

To achieve      this  flexibility,        !WORD] uses anoth~ointer              in
addition   to i>INI, called      iBLKI (pronounced    b-1-k).     ~ acts both
as a flag and as a pointer.
                                                     rw
                                       If !BLKI contains
scans the input message buffer (that is,
if iBLKI contains    a non-zero
                                                              zero, then iWORDI
                                                         of,set
                                     number, then WORD is referring
                                                                   by i>IN!). But
                                                                              to a
block buffer and the number in iBLK! is the number of the block.
Here are two examples:


      contents   of   address    currently   used by WORD:
           BLK

           0              so@    >IN@+
                            (>IN bytes into       the message     buffer)

           200            200 BLOCK >IN@           +
                            (>IN bytes into       the block   buffer)


Every time a word is interpreted           during a !LOAD!operation,           iWORDi
makes sure that the appropriate          block is still in a buffer.

A useful word to use in conjunction     with jwoRpl is !COUNT!. Recall
that   WORD leaves  the length    of the word in the first     byte of
 WORD's buffer and also leaves      the address  of this byte on the
stack.




The word iCOUNTj puts      the   count   on the    stack    and   increments     the
address, like this:
10 I/0 AND YOU                                                                                 281




leaving     the stack      with a string    address                       and    a count            as
appropriate    argum e nts for !TYPE!, !CMOVE!,etc.
[COUNT! is used in the            definition           of !TEXT! which          we gave       in a
footnote  earlier.

  COUNT                 (adr -- adr+l        u)        Converts          a character
                                                       string,      whose length           is
                                                       contained          in its     first
                                                        byte,       into      the     form
                                                       appropriate         for TYPE, by
                                                       leaving     the address of the
                                                       first   character          and the
                                                       length on the stack.

We will    further   illustrate      the   use    of    !WORDI in   one    of    the     examples
in Chap. 12.



String    Comparisons


Here is a FORTH word that                  you can       use to compare                character
strings:

  -TEXT                 (adrl     u adr2 -             Compares      two strings
                          f)                           that start     at adrl and
                                                       adr2, each of length u.
                                                       Returns    false   if they
                                                       match~ true if no match
                                                       (positive       if binary
                                                       string    1 > 2, negative
                                                       if 1 < 2).
282                                                                   Starting     FORTH




!-TEXT! can be used to test either   whether two character       strings
are equal or whether one is alphabetically    greater   or lesser than
the other. tt   Chap. 12 includes   an example    of using 1-TEXTI to
determine  whether strings match exactly.
Since for speed PfExTj compares cell-by-cell,              you must take care
on cell-address         machines to give 1-TEXTI even cell addresses     only.
For example,          if you want to compare       a string     that is being
entered        as input with a strin~t          is in an ar~ring           the
~t        string    to the pad (using ~ rather          than lliQBQ]) because
~ is an even            address.   Similarly, if you want to test a string
that     is in a block buffer,       you must either     guarantee   that the
string's      address is even or, if you cannot know for sure, move the
string to an even address (using !CMOVE!)before making the test.
By the   way, the hyphen in !-TEXT! is as close as ASCII comes to
11
     -,the logical
          11
               ,           symbol    meaning    "not."     This is why we
conventionally      use this prefix for words which return a "negative
true" flag.      (Negative    true means that a zero represents    true and
a non-zero     represents    false.)   We pronounce    such words not - text,
etc.




tFor Users of Intel,              DEC, and Zilog     Processors

To make the             "alphabetical"    test,    you must first   reverse      the order
of bytes.

tFORTH-79 Standard
-TEXT is not included    in the Standard.                    If your system does not
have -TEXT      ou can load the high-level                     definition  below. Of
course,  -TEXT is written     in assembler                  code on all polyFORTH
systems, for speed.
                   -TEXT   2DUP + SWAP DO DROP 2+
                      DUP 2- @ I @ - DUP IF DUP ABS /             LEAVE THEN
                          2 +LOOP SWAP DROP 7
10 I/0   AND YOU                                                        283




Here's a list of the FORTH
                         words covered in this chapter.
  UPDATE           (   - )          Marks the most recently
                                     referenced       block     as
                                    modified.     The block will
                                    later     be automatically
                                    transferred   to mass storage
                                    if its buffer is needed to
                                    store a different     block or
                                    if FLUSH is executed.

  EMPTY-BUFFERS( -        )         Marks all block buffers as
                                    empty without necessarily
                                    affecting    their  actual
                                    contents.   Updated blocks
                                    are not written    to mass
                                    storage.
  BLOCK            <p-- adr)        Leaves the address of the
                                    first byte in block u. If
                                    the block is not already in
                                    memory, it is transferred
                                    from mass storage          into
                                    whichever      memory buffer
                                    has been least       recently
                                    accessed.       If the block
                                    occupying    that buffer has
                                     been     updated       (i.e.,
                                    modified),    it is rewritten
                                    onto   mass   storage      before
                                    block u is read         into   the
                                    buffer.
 BUFFER            u -   adr)       Obtains   the next block
                                    buffer,  assigning      it to
                                    block u. The block is not
                                    read from mass storage.
  TYPE             (adr u --    )   Transmits     u characters,
                                    beg inning    at address,    to
                                    the current   output device.
  -TRAILING        (adr ul --       Eliminates trailing blanks
                      adr u2)       from the string that starts
                                    at the address by reducing
                                    the count from ul (original
                                     byte     count)    to     u2
                                    (shortened byte count).
284                                                   Starting    FORTH




 MOVE          (adrl adr2 u --   )   Copies a region of memory
                                     u bytes long, cell-by-cell
                                     beginning      at adrl,      to
                                     memory beginning    at adr2.
                                     The move begins with the
                                     contents      of adrl      and
                                     proceeds     toward     high
                                     memory.
 CMOVE         (adrl adr2 u -    )   Copies a region of memory
                                     u bytes long, byte-by-byte
                                     beginning      at adrl,     to
                                     memory beginning     at adr2.
                                     The move begins     with the
                                     contents      of adrl     and
                                     proceeds     toward     high
                                     memory.
 KEY           (   --   c)           Returns the ASCII value of
                                      the    next     available
                                     character    from the current
                                     input device.
 EXPECT        (adr u --     )       Awaits u characters        (or a
                                     carriage    return)    from the
                                     terminal      keyboard      and
                                     stores   them, starting       at
                                     the address.
 WORD          (c -- adr)            Reads one word from the
                                     input     stream,    using     the
                                     character      (usually    blank)
                                     as a delimiter.        Moves the
                                     string      to the      address
                                      (HERE) with the count in
                                     the first byte, leaving the
                                     address on the stack.
 TEXT          (c -      )           Reads a string       from the
                                     input     stream,   using    the
                                     character      as a delimiter,
                                     then sets the pad to blanks
                                     and moves the string to the
                                     pad.
  >BINARY or   (dl adrl --           Converts      the text begin-
  CONVERT        d2 adr2)            ning at adrl+l to a binary
                                     value with regard to BASE.
                                     The      new        value         is
                                     accumulated       into dl, being
                                     left    as d2; adr2 is the
                                      address        of the       first
                                     non - convertible      character.
10 I/0   AND YOU                                                            285




   NUMBER          ~adr - - n or d)         Converts         the    text
                                            beg inning    at adr+l, with
                                            regard to BASE, to a binary
                                            value that is single-length
                                            if no valid     punctuation
                                            occurs, and double-length
                                            if valid punctuation      does
                                            occur.      The string      may
                                            contain      a preceding
                                            negative     sign;   adr may
                                            contain a count, which will
                                            be ignored.
   COUNT           / adr -- adr+ 1 u}       Converts        a character
                                            string,     whose length        is
                                            contained        in its first
                                             byte,     into      the    form
                                            appropriate       for TYPE, by
                                            leaving the address of the
                                            first   character        and the
                                            length on the stack.

Additional   Words Available   in Some Systems
   >TYPE           (adr u -                 Same as TYPE except that
                                            the output string is moved
                                            to the pad prior to output.
                                            Used in multiprogrammed
                                            systems to output strings
                                            from disk blocks.
   <CMOVE          (adrl adr2 u -       }   Copies a region of memory
                                            u bytes long, beginning    at
                                            adrl, to memory beginning
                                            at adr2, but starts   at the
                                            end of the string       and
                                            proceeds      toward     low
                                            memory.
   -TEXT           (adrl u adr2 -           Compares         two strings
                     f}                     that    start     at adrl     and
                                             adr2, each of length           u.
                                            Returns       false     if they
                                            match; true if no match
                                            (positive if binary string 1
                                            > 2, negative      if 1 < 2).
   BLANK           (adr n -    }            Stores ASCII blanks into n
                                            bytes of memory, beginning
                                            at adr.
286                                                        Starting   FORTH




Review of Terms

Buffer
status cell             in the FORTH operating         system,    a cell in
                        resident    memory associated      with each block
                        buffer (usually directly   preceding   it in memory)
                        which     contains    the number of the block
                        currently    stored in the buffer and a flag (the
                        sign bit) which indicates       whether the buffer
                        has been updated.
Relative      pointer   a variable      which specifies   a location    in
                        relation   to the beginning of an array or string
                        --not the absolute address.
Superstring             in FORTH, a character      array which contains a
                        number of strings.       Any one string    may be
                        accessed by indexing    into the array.
Virtual    memory       the treatment of mass storage    (such as the disk)
                        as though it were resident      memory; also the
                        mechanisms of the operating     system which make
                        this treatment possible.
10 I/0 AND YOU                                                                 287




Problems    -   Chapter     10


1.   Enter some famous quotations     into an available    block, say
     228. Now define   a word called   CHANGE which takes two ASCII
     values and changes   all occurrences   within block 228 of the
     first character into the second character.     For example,

            65 69 CHANGE

     will   change    all   the    "A"s into     "E"s.
2.   Define a word called         FORTUNE which will print    a prediction
     at your terminal,       such as "You will receive    good news in the
     mail."     The prediction       should be chosen    at random from a
     list of sixteen       or fewer predictions.       Each prediction     is
     sixty-four    characters,     or less, long.
3.   According to Oriental          legend, Buddha endows all persons born
      in each       year     with   special,    helpful     characteristics
     represented         by one of twelve animals.        A different       animal
     reigns     over each year,         and every twelve      years the cycle
     repeats     itself.      For instance,   persons born in 1900 are said
     to be born            in the     "Year  of the     Rat."       The art      of
     fortune-telling         based on these influences      of the natal year
     is called      "Juneeshee."

     Here is the order           of the cycle:
            Rat Ox Tiger Rabbit Dragon Snake
            Horse Ram Monkey Cock Dog Boar

     Write a word called               .ANIMAL that      types   the name of the
     animal corresponding             to its position      in the cycle as listed
     here; e.g.,

            0   .ANIMAL RAT ok

     Now write       a word       called   (JUNEESHEE) which takes    as an
     argument        a year       of birth    and prints  the name of the
     associated       animal.      (1900 is the year of the Rat, 1901 is the
     Ox, etc.)
     Finally,  write a word called     JUNEESHEE which prompts the
     user for his/her   year of birth     and prints the name of the
     person's Juneeshee    animal.   Define it so the user won't have
     to press "return"  after entering    the year.

4.   Rewrite     the definition       of LETTER that    appears     in this
     chapter    so that it uses names and personal     descriptions     that
     have been edited         into a block,   rather than entered      into
     character     arrays.    In this way, you can keep a file on many
     "prospects"     and produce a letter    for any one person with the
288                                                           Starting         FORTH




      appropriate   descriptions,   just     by supplying     an argument          to
      LETTER, as in

               1 LETTER
      Now define  LETTERS so that          it prints   one   letter      for    each
      person in your file.

5.    In this exercise   you will create          and use a virtual     array,
      that is, an array which resides            on the disk but which is
      referenced  like a memory-resident        array (with [fil and []).
      First   select   an unused block in your range        of assigned
      blocks.    There can be no text on this block; binary data will
      be stored in it.      Put this block number in a variable.     Then
      define   an access word which accepts        a cell subscript  from
      the stack, then computes the block number corresponding           to
      this subscript,    calls iBLOCKi and returns    the memory address
      of the subscripted      cell.  This access word should also call
      iUPDATEi. Test your work so far.
      Next use the first cell as a count of how many data items are
      stored  in the array.   Define a word PUT which will store a
      value into the next available     cell of the array.   Define a
      display  routine  which will print the stored elements   in the
      array.
      Now use this virtual   array facility to define a word ENTER
      which will accept    pairs of numbers and store them in the
      array.

      Finally, define TABLE to print        the data   entered        above,    eight
      numbers per line.
                       11 EXTENDING THE COMPILER:
                    DEFINING   WORDS AND COMPILING WORDS


In comparison     with traditional        languages,      FORTH's compiler         is
completely    backwards.     Traditional       compilers     are huge programs
designed   to translate      any foreseeable,          legal    combination       of
available   operators    into machine language.             In FORTH, however,
most of the work of compilation           is done by a single        definition,
only a few lines long.       Special     structures     like conditionals        and
loops are not compiled        by the compiler        but by the words being
compiled ([!fil, [QQJ,etc.).

Lest you scoff     at FORTH's simple     ways, notice   that FORTH is
unique among languages    in the ease with which you can extend the
compiler.    Defining   new, specialized      compilers  is as easy as
defining  any other word, as you will soon see.

When you've    got      an extensible         compiler,     you've    got   a very
powerful language!



Just   a Question    of Time


Before we get fully into this chapter, let's review one particular
concept   that can be a problem to beginning    FORTH programmers.
It's a question  of time.

We have used the term "run time II when referring        to things   that
occur when a word is executed    and "compile    time II when referring
to things that happen when a word is compiled.          So far so good.
But things get a ~ittle confusing    when a single      word has both a
run-time behavior and a compile-time   behavior.

In general    there are two classes  of words which behave in both
ways.   For purposes    of this discussion,    we'll call these two
classes  "defining  words" and "compiling   words."

A defining   word is a word which, when executed,     compiles  a new
definition.      A defining    word specifies the compile-time    and
run-time behavior    of each member of the "family" of words that it
defines.    Using the defining    word ICONSTANTIas an example, when
we say

       80 CONSTANT    MRGIN
                      i
                                        289
290                                                              Starting      FORTH




we are executing  the compile-time   behavior  of !CONSTANT!:that is,
!CONSTANT! is compiling    a new constant-type     dictionary   entry
called  MARGIN and storing   the value 80 into its parameter   field.
But when we say
      MARGIN

we   are executing    the run-time  behavior  of !CONSTANT!: that is,
!CONSTANT! is pushing     the value 80 onto the stack.  We'll pursue
defining   words further in the next few sections.
The other      type of word which possesses     dual behavior  is the
"comp .Hing word."      A compiling word is a word that we use inside
a colon     definition    and that  actually  does something   during
compilation     of that definition.

One example        is the word ~,        which at compile       time compiles        a
text string      into the dictionary       entry with the count in the first
byte,      and at run time           types      it.   Other      examples        are
control-structure          words like [TI:] and jLOOPI, which also have
compile-time        behaviors   distinct     from their    run-time    behaviors.
We'll explore         compiling   words after       we've discussed       defining
words.



How to Define      a Defining     Word


Here are the standard        FORTH defining      words we've     covered       so far:

      VARIABLE
      2VARIABLE
      CONSTANT
      2CONSTANT
      CREATE
      USER

What do they all have in common? Each of them is used to define
a set      of words with similar compile-time    and run-time
characteristics.
And how are all these defining           words defined?        First   we'll    answer
this question metaphorically.
Let's say you're in the ceramic salt - shaker business.        If you plan
to make enough salt shakers,       you'll    find it's easiest   to make a
mold first.     A mold will guarantee     that all your shakers will be
of the same design,     while allowing        you to make each shaker      a
different   color.
11 EXTENDINGTHE COMPILER                                                           291




In making the mold, you must consider                two things:

     1.     How the mold will work. (E.g., how will you get the clay
            into and out of the mold without   breaking  the mold or
            letting the seams show?)

     2.     How the shaker will work.  (E.g., how many holes                  should
            there be? How much salt should it hold?   Etc.)

To bring this analogy back to FORTH, the definition     of a defining
word must specify  two things:   the compile-time   behavior  and the
run-time behavior  for that type of word.                     --

Hold that thought a moment while we look at the most basic of the
~~fi~in[   words in the above list:   JCREATEI. At compile    time,
 CREATE takes      a name from the input  stream  and creates       a
  1ct1onary heading for it.



            !CREATE)EXAMPLE




                                               r
                          7            E
                                                      JCREATEjrun-time
                          X            A              code (when
                                link                  executed,   pushes
                                                      the potential
                          code pointer                pfa onto the
          (pfa) ___,___                        :      stack).
                 L---     -- -- - - -- ----<




At run time,     ICREATEIpushes            the pfa of EXAMPLE onto    the stack.

What happens         if we use !CREATE! inside    a definition?            Consider
this example,       which is the definition   for !VARIABLE!:
     : VARIABLE               CREATE 2 ALLOT ;
292                                                           Starting   FORTH




When we execute    !VARIABLE) as in

      VARIABLE ORANGES

we are indirectly   using [CREATE) to create     a dictionary    head with
the name ORANGES and a code pointer          that points      to !CREATE!' s
run-time code.    Then we are allotting    two bytes for the variable
itself.

Since the run-time   behavior of a variable is identical to that of
a word defined     by )CREATE!, VARIABLE does not need to have
run-time code of its own; it can use CREATE 's run-time code.

How do we specify  a different run-time   behavior              in a defining
word? By using the word JDOES>J, as shown here:


       DEFINING-WORD      CREATE (compile-time   operations)
                          DOES> (run-time operations)


To illustrate,   the following      could be a valid    definition               for
!CONSTANT! (although     in fact    JCONSTANTJ is usually     defined              in
machine code) :
      : CONSTANT    CREATE ,    DOES> @ ;

To see how this definition works,       imagine    we're   using   it to define
a constant named TROMBONES, like        this:


      76 CONSTANT TROMBONES


                     CREATE           Creates  a new dictionary          entry
  compile-                            (e.g., TROMBONES).
  time
  portion                             Compiles the value (e.g., 76) for
                                      the constant     from the stack
                                      into the constant's   parameter
                                      field.

                     DOES>            Marks       the      end    of    the
                                      compile-time      behavior     and the
  run-                                beginning        of the    run-time
  time                                behavior.       At run time, !DOES>)
  portion                             will leave     the pfa of the word
                                      being defined      on the stack.

                                      Fetches      the contents    of the
                                      constant,      using  the pfa that
                                      will    be   on the stack    at run
                                      time.
11 EXTENDING
           THE COMPILER                                                                      293




The words that    recede  DOES> specify   what the mold will do; the
words that follow     DOES> specify   what the product  of the mold
will do.


  DOES>                run time:                    Used     in creating          a
                       ( -- adr)                    defining       word; marks
                                                    the end of its compile-
                                                    time portion        and the
                                                    beginning        of its run-
                                                    time portion.       The run-
                                                    time     operations        are
                                                    stated    in higher-level
                                                    FORTH. At run time, the
                                                    pfa of the defined        word
                                                    will be on the stack.



                                                                                         f)1
Defining     Words You Can Define             Yourself                              I~




Here are     some examples           of defining         words   that     you can        create
yourself.

Recall that in our discussion    of "String Input Commands" in Chap.
10, we gave an example      that employed   character-string        arrays
called      NAME, EYES, and ME. Every time we used one of these
names, we followed      it with a character     count.       In the input
definition,    we wrote

        ..• PAD NAME 14 MOVE

and in the output       definition       we wrote

        ••• NAME 14 -TRAILING TYPE

and so on.

Let's eliminate   the count by creating                     a defining word called
CHARACTERS, whose product definitions                    will leave the address and
count on the stack when executed.

We'll    use it like   this:    if we say

        20 CHARACTERSME

we will create    an array           called    ME, with       twenty    bytes      available
for the character   string.

When we execute        ME, we'll        get   the   address      of the    array         and the
294                                                             Starting    FORTH




count     on the stack.   Now we can write:
         PAD ME MOVE

instead        of
         PAD ME 20 MOVE

or

         ME -TRAILING TYPE

instead        of

         ME 20 -TRAILING TYPE

Here's     how we might define     CHARACTERS:

                      CHARACTERS

                          CREATE              Creates    a new dictionary
                                              entry {e.g., ME).

                          DUP , ALLOT         Compiles       the count       (e.g.,
     compile-                                 twenty)     into the first       cell
     time                                     of the      array      for   future
     portion                                  reference.        Then allots        an
                                              additional      twenty bytes be-
                                              yond     the     count     for    the
                                              string.
                          DOES>               Marks    the    beginning           of
                                              run-time    code,   leaving        the
                                              pfa of the product-word             on
                                              the stack at run time.
     run-
     time                 DUP                 Copies   the pfa.
     portion
                          2+                  Advances        the    address     to
                                              point past     the    count,   to the
                                              start    of    the     character
                                              string.
                          SWAP@               Swaps the string      address with
                                              the     count    address       and
                                              fetches    the count.    The stack
                                              now holds {adr count -- ) .
11 EXTENDINGTHE C1 MPILER                                                 295




We've just extended      our compiler!    Our new word CHARACTERS is a
defining     word that creates   a data structure and procedure  that we
find useful.      CHARACTERSnot only simplifies     our input and output
definitions,     it also allows us to change the length of any string,
should the need arise,        in one place only (i.e., where we define
it).
Our next example could be useful in an application         where a large
number of byte arrays are needed.   Let's create         a defining word
called  STRING as follows:

     : STRING    CREATE ALLOT DOES> +

to be used in the form
     30 STRING VALVE

to create  an array thirty bytes     in length.    To access   any byte    in
this array, we merely say:
     6 VALVE C@

which would give us the current     setting    of hydraulic    valve 6 at
an oil-pumping   station. At run time, VALVE will add the argument
6 to the pfa left by~,        producing     the correct   byte address.
If our application       requires    a large   number of arrays       to be
initialized    to zero, we might     include  the initialization      in an
alternate   defining   word called   0STRING:


       ERASED HERE OVER ERASE ALLOT ;
       0STRING CREATE ERASED DOES> + ;


First    we define  ERASED to ERASE the given     number of bytes,
starting   at IHEREI, before ALLOTting the given number of bytes.
Then we simply   substitute   ERASED for IALLOTIin our new version.

By changing      the definition     of a defining    word, you can change
the characteristics      of all the member words of that family.        This
ability   makes program development       much easier.    For instance,  you
can incorporate      c rtain    kinds of error checking      while you are
developing     the pr gram, then eliminate        them after you are sure
that the progra~ ru s correctly.
Here is a version   f STRING which,       at run time,   guarantees    that
the index into the array is valid:


       STRING CRE , TE DUP , ALLOT
        DOES> 2DUP @ U< NOT ABORT" RANGEERROR " + 2+
296                                                     Starting   FORTH




which breaks down as follows:

      DUP , ALLOT                       Compiles    the count  and
                                        allots  the given number of
                                        bytes.
      DOES> 2DUP@                       At run time,    given   the
                                        argument    on the stack,
                                        produces:
                                           (arg pfa arg count -- ) •
      U< NOT                            Tests that the argument is
                                        not less than the maximum,
                                        i.e.,  the stored      count.
                                        Since IU<I is an unsigned
                                        compare,        negative
                                        arguments   will appear       as
                                        very high numbers and thus
                                        will also fail the test.
      ABORT" RANGEERROR"                Aborts if the     comparison
                                        check fails.
      + 2+                              Otherwise   adds the argu-
                                        ment to the pfa, plus an
                                        additional two to skip over
                                        the cell that contains  the
                                        count.


Here's another way that the use of defining words can help during
development.     Let's say you suddenly       decide  that all of the
arrays you've defined     with STRING are too large to be kept in
computer memory and should be kept on disk instead.        All you have
to do is redefine     the run-time    portion   of STRING. This new
STRING will compute which block on the disk a given~would
be contained   in, read the block into a buffer using ~'             and
return the address     of the desired     byte within   the buffer.     A
string defined    in this way could span many consecutive        blocks
(using the same technique as in Prob. 5, Chap. 10).
You can use defining words to create all kinds of data structures.
Sometimes, for instance,     it's useful to create multi-dimensional
arrays.    Here's an example of a defining        word which creates
two-dimensional   byte arrays of given size:
11 EXTENDINGTHE COMPILER                                                                297




       ARRAY ( #rows #cols --                 )
           CREATE OVER , * ALLOT
           DOES> ( member: row col --
           DUP @ ROT * + + 2+ ; t


                   columns
                                                  To create   an array four bytes        by
           0       1    2        3
                                                  four bytes, we would say
       0
                                                      4 4 ARRAY BOARD
       1
rows                                              To access, say, the byte       in row 2,
       2           ?                              column 1, we could say
                    •
       3
                                                      2 1 BOARD C@



Here's    how our ARRAY works in                       column:   0     1     2      3
general        terms.     Since     the
computer     only allows us to have                              0     4     8    12
one-dimensional       arrays,   we must
simulate     the second     dimension.                           1     5     9    13
While our imaginary        array looks
like this:----------•                                            2     6   10     14
                                                                 3     7   11     15


our real   array       looks   like   this:




If you want the address   of the byte in row 2, column 1, it can be
computed by multiplying    your column number (1) by the number of
rows in each column (4) and then adding your row number (2), which
indicates  that you want the sixth byte in the real array.


t For Optimizers
This version       will   run even      faster:

       ARRAY OVER CONSTANT HERE 2+ ,                         * ALLOT
         DOES> 2@ ROT * + + ;
298                                                                  Starting     FORTH




This calculation    is what members of ARRAY must do at run time.
You'll notice that, to perform this calculation,     each member word
needs to know how many rows are in each column of its particular
array.    For this reason,  ARRAY must store     this value into the
beginning   of the array at compile time.

For the curious,  here             are   the   stack   effects      of the      run-time
portion of ARRAY:


                       Contents
      o:eeration       of Stack
                       row col pfa
      DUP@             row col pfa #rows
      ROT              row pfa #rows col

      *                row pfa col-index

      + +              address
      2+               corrected-address

It is necessary   to add two to the computed address     because                         the
first cell of the array contains  the number of columns.

Our final    example      is the    most visually      exciting,     if not the         most
useful.

  0   (   SHAPES, USING A DEFINING WORD)                    EMPTY
  1
  2       STAR     42 EMIT ;
  3       .ROW     CR 8 0 DO DUP 128 AND
  4                 IF STAR ELSE SPACE THEN
  5                             2* LOOP DROP ;
  6
  7       SHAPE    CREATE 8 0 DO C,  LOOP
  8                DOES> DUP 7 + DO IC@ .ROW -1 +LOOP                              CR
  9
 10 HEX       18 18 3C SA 99 24 24 24 SHAPE MAN
 11           81 42 24 18 18 24 42 81 SHAPE EQUIS
 12           AA AA FE FE 38 38 38 FE SHAPE CASTLE
 13                                                                              DECIMAL

.ROW prints  a pattern  of stars and spaces                that    correspond      to the
8-bit number on the stack.    For instance:
11 EXTENDING
           THECOMPILER                                                       299




     2 BASE !~
     00111001  • ROW_
          *** * Dk
     DECIMALok
Our defining    word SHAPE takes eight arguments from the              stack and
defines   a shape which, when executed,    prints an 8-by-8            gr id that
corresponds    to the eight arguments.  For example:
      MAN
        **
        **
       ****
      * ** *
     * ** *
       * *
       * *·
       * *
     Ok
In summary, defining    words can be extremely   powerful tools.     When
you create    a new defining       word, you extend     your compiler.
Traditional   languages    do not provide   this flexibility     because
traditional  compilers    are inflexible  packages   that say, "Use my
instruction set or forget it!"
The real power of Jdefining         words is that they can simplify       your
problem.      Using them well, you can shorten     your programming time,
reduce      the size Of your program,        and improve     readability.
FORTH' s flexibility       in this regard is so radical  in comparison       to
traditional      languages     that many people   don't even believe        it.
Well, now you've seen it.

The next section   introduces          still   another    way to   extend    the
ability of FORTH's compiler.



How to Control     the   Colon   Compiler


Compiling     words are words used inside        colon definitions      to do
something      at compile      time.    The most obvious       examples    of
compiling!    words are control-structure       words such as !!!], ITHENI,
fi5ol, LOOP, etc. Because FORTH programmers don't often change
the way these particular          words work, we 're not going to study
them any further.      Instead    we'll examine the group of words that
control    the colon compiler        and thus can be used to create       ~
type of compiling    word.

Recall that the coion compiler ordinarily              looks up each   word of a
source     definition        and compiles    each   word's   address   into the
dictionary       entry--that's     all.   But the   colon compiler     does not
300                                                                                      Starting       FORTH




compile        the address         of a compiling                  word--it     executes       it.

How does the colon compiler         know the difference?        By checking
the definition's       "precedence     bit."    If the bit is "off,"      the
address of the word is compiled.          If the bit is "on," the word is
executed   immediately;     such words are called    "immediate"   words.

The word !IMMEDIATE! makes a word "immediate."                                         It is used           in the
form
          name        definition           ;      IMMEDIATE

that     is,    it   is    executed              right           after   the     compilation            of        the
definition.

To give        an immediate          example,            let's      define

         : SAY-HELLO              ." HELLO II •,             IMMEDIATE

We can execute    SAY-HELLO interactively,                                     just   as we could            if     it
were not immediate.
         SAY-HELLO HELLO ok

But if we put SAY-HELLO                           inside           another       definition,           it     will
execute at compile time:

         : GREET          SAY-HELLO . 11 I SPEAK FORTH II                             HELLO ok

rather     than      at execution              time:
         GREET I SPEAK FORTH ok

Before    we go on, let's     clarify     our terminology.      FORTH folks
adhere    to a convention        regarding     the terms "run time"       and
"compile    time. 11 In this example,      the terms are defined   relative
to GREET. Thus we would say that SAY-HELLO has a "compile-time
behavior"     but no "run-time     behavior."     Clearly,   SAY-HELLO does
have run-time     behavior   of its own, but relative      to GREET it does
not.
To keep our levels     straight, let's call GREET in this example the
"compilee";     that   is, the definition   whose compilation        we're
referring   to.   SAY- HELLO has no run-time behavior    in relation     to
its compilee.

Here's an example of an immediate word that you're familiar                                                  with:
the definition   of the compiling word IBEGINI, It's simpler                                                 than
you might have thought:
         : BEGIN          HERE ;          IMMEDIATE

[BEGIN]
      simply              saves     the        address       of IHEREI at compile               time        on the
ll EXTENDING THE COMPILER                                                                             301


                                                                                                  j

stack.     Why? Because     sooner   or later  an !UNTIL! or IREPEATI is
going to come along,      and either   has to know what address   in the
dictionary    to return to in the event that it must repeat.     This is
the address that !BEGIN! left on the stack.
BEGIN's compile-time    behavior                    is leaving~            on the stack.    But
BEGIN compiles    nothing   into                   the compilee;       there   is no run-time
behavior for IBEGINj.

Unlike !BEGIN!, most compiling   words do have a run-time behavior.
To have a run-time     behavior,   a word has to compile   into the
compilee the address of the run-time behavior,   which must already
have been defined   as a word.

A good jxam§le  ij             (i55).i
                         Like BEGIN, IQQjmust provide,  at compile
time, a HERE for LOOP or +LOOP to return to. But unlike IBEGINI,
~ also has a run-time    behavior: it must push the limit and the
index onto the return stack.

The run-time   behavior
sometimes called
                         o!    is defined    im
                                             by a lower-level
                   [@QI]or 2> • The definition   of [QQ]is this:
                                                                 word,

          : DO       COMPILE 2>R          HERE ;      IMMEDIATE

The word !COMPILE! finds the address        of the                                      2>R
next word in the definition       (in this case
!2>R!) and compiles    its address     into    the
compilee   definition,    so that   at run time
                                                                            compilee definition
~ will be executed.t


t For the       Very Curious
Another  example    is the            definition     of   [i]. At compile      time,     semicolon
must do two things:

     1. .       compile the address          of JEXITI into    the   dictionary-entry         being
                compiled, and

         2.     leave   compilation       mode.

Here's        the definition    of semicolon:

                 COMPILE EXIT         R> DROP ;      IMMEDIATE

The first phrase compiles     JEXITI, providing   the run-time    behavior.    The
second phrase , which is the compile-time        behavior,   gets us out of the
compiler.    The top return address at this moment is pointing          inside the
colon compiler,    which is simply a JBEGINJ••• JUNTILI loop.     When semicolon
has finished    being executed,    execution    wil l return   not to the colon
compiler,   but to !INTERPRET!.
Don't        worry     about   how we can use a semicolon         to end the very
d e f i n i t i on that defines   it. The e xplanation r e quire s an understanding
of pol y FORTH' s Target Compil e r, whi ch i s beyond the scope of thi s book
(see Appendix 2).
302                                                                   Starting      FORTH




Another compiler-controlling       word is l[COMPILE]l.t This word can
be used to compile       an immediate     word as though  it were not
immediate.  Given our previous      example, in which SAY-HELLO is an
immediate definition,     we might define
       : GREET   [COMPILE] SAY-HELLO • " I SPEAK FORTH " : ok

to force   SAY-HELLO to               be compiled     rather   than      executed      at
compile time.  Thus:

       GREET HELLO I SPEAK FORTH ok

Be sure you understand         the difference       between     iCOMPILEl and
i[COMPILE]l.        lCOMPILEl       compiles        the     address    of any
(non-immediate)      word into a compilee       definition:      think of it as
deferred    compilation.      i[COMPILE)I compiles        the address    of any
immediate word into the definition          currently     being defined;    this
is ordinary   compilation,    but of an immediate word which otherwise
would have been executed.
To review, here are          three     words which    are useful   in creating        new
compiling  words:


  IMMEDIATE          ( --        )         Marks     the    most  recently
                                           defined      word as one which,
                                           when encountered           during
                                           compilation,     will be executed
                                           rather than be compiled.
  COMPILE XXX        (   -       )         used in the definition          of a
                                           compiling     word.     When the
                                           compiling    word, in turn,         is
                                           used in a source      definition,
                                           the code field address of xxx
                                           will    be compiled      into     the
                                           dictionary   entry so that when
                                           the new definition         is exe----
                                           cuted, xxx will be executed.           br«cktt·
                                                                                  compile-
  [COMPILE] xxx              -   )         Used in a colon      definition,       brockrt
                                           causes the immediate word xxx I
                                           to be compiled      as though       it
                                           were not immediate:       xxx will      ~
                                           be executed    when the defini-           ~
                                           tion is executed.




tFor   Some Small-system,            Non-polyFORTH,   Users
See footnote,    page    218.
11 EXTENDING THE COMPILER                                               303




More Compiler-controlling         Words


As you may recall,      a number that appears  in a colon definition      is
called a "literal."       An example is the "4" in the definition

      : FOUR-MORE       4 + ;

The use of a literal           in a colon
definition       requires      two cells.
The first      contains     the address
                                                      9             F
of a routine            which,      when              0             u
executed,      will push the contents                        link
of the second         cell   (the number
itself)    onto the stack.t                           code pointer

                                                          (LITERAL)
The name of this         routine    may
vary; let's    call it the "run-time                         4
code for a literal,"         or simply
J(LITERAL)J.        When the colon                           +
compiler    encounters    a number, it                      EXIT
first compiles      the run-time   code
for a literal,     then compiles     the
number itself.

The word you will      use most often to compile a literal   is ILITERALI
(no parentheses).       ILITERAL! compiles both the run-time    code and
the value itself.      To illustrate:

      4   : FOUR-MORE       LITERAL + ;
Here the word ILITERALI will compile     as a literal    the "4" that we
put on the stack     before  beginning      compilation.       We get a
dictionary entry that is identical    to the one shown above.
For a more useful application      of JLITERALI, recall   that in Chap. 8
we created    an array called    LIMITS that consisted      of five cells,
each of which contained       the temperature     limit for a different
burner.    To simplify   access    to this array,    we created     a word
called   LIMIT. The two definitions     looked like this:




t For Memory Conservationists
While a literal       requires  two cells,  a reference      to a constant
requires    only one cell.     Since a constant     takes only five cells
to define,    you can see that if you're going to use the same value
six times or more, you will save memory by defining            the value as
a constant.      There is hard l y any difference        between   the time
required    to execute a constant    and a literal.
304                                                         Starting   FORTH




       VARIABLE LIMITS 8 ALLOT
       : LIMIT  2* LIMITS + ;


Now let's  assume that we will only access    the array through  the
word LIMIT. We can eliminate     the head of the array (eight bytes)
by using this construction instead:


       HERE 10 ALLOT
       : LIMIT  2* LITERAL +


In the first    line   we put the address   of the beginning      of the
array   (!HERE!) on the stack.   In the second   line, we compile    this
address   as a literal  into the definition  of LIMIT.


      old                        ne"'
 version                   version
             heaclfor                      s
             LIMITS                      ce Ils


                 S"                                    Because    we had to
                                        headfor
             cells                                     add an extra      cell
                                        LIMIT          for the literal      to
                                                       the definition        of
                                                       LIMITS,      our   net
                                                       saving      is three
             head for                   (LITERAL)      cells.
             LIMIT                        adr

                 2*
                                          +
                                        EXIT
             LIMITS
                 +
             EXIT

There are two other compiler     control    words you should know. The
words
compilation
            rn
            and !TIcan be used inside
                and start it again,
                                           a colon
                                       respectively.
                                                      definition
                                                            Whatever
                                                                     to stop
                                                                         words
appear    between   them will be executed        "immediately,"      i.e.,   at
compile time.

Consider     this     example:
       : SAY-HELLO • II HELLO II ;
       : GREET [ SAY-HELLO ] . " I SPEAK FORTH "            HELLO ok
       GREET I SPEAK FORTH ok
11 EXTENDING THE COMPILER                                                             305




In this     example, SAY-HELLO is not           an immediate word,      yet    when we
compile      GREET, SAY-HELLO executes           "immediately."

For a better   example, imagine a colon definition   in which                           we
need to type line 3 of block 180. To get tne address   of line                          3,
we could use the phrase

        180 BLOCK 3 64 * +
but it's     time-consuming     to execute

        3 64 *

every      time we use this     definition.      Alternatively,     we could    write

        180 BLOCK 192 +

but it's     unclear     to human readers      exactly   what the 192 means.



The best      solution    is to write
                                                                    (LITERAL)
        180 BLOCK [ 3 64 * ] LITERAL +
                                                                        192
Here the arithmetic    is performed             only once,
at compile    time, and the result            is compiled
as a literal.


Here's    a silly   example       which may give         you some ideas for more
practical     applications.         This definition         must be loaded from a
disk block:

           LIST-THIS       [ BLK @ J    LITERAL LIST ;

When you execute      LIST-THIS,     you will  list whichever    block
LIST-THIS is defined     in.   (At com ile time, iBLK! contains     the
number of the block being loaded.       LITERAL compiles   this number
into the definition    as a literal,    so that it will serve   as the
argument for !LIST! at run time.)


By the way, here's         the definition      of JLITERALI:
           LITERAL       COMPILE (LITERAL)        , ;    IMMEDIATE

First   it compiles          the address       of the    run-time    code,     then     it
compiles the value          itself (using     comma).
306                                                                   Starting     FORTH




To summarize, here are the            additional      compiler     control       words we
introduced  in this section:

  LITERAL            compile       time:           Used      only      inside    a
                     (n -      )                   colon      definition.      At
                     run time:                     compile      time, compiles
                     (    -   n)                   a value from the stack
                                                   into the definition          as
                                                   a literal.        At run time,
                                                   the      value        will  be
                                                   pushed onto the stack.

                                                   Leaves   compile     mode.

                                                   Enters   compile     mode.




                                   A Handy Hint

          Entering       Long Definitions          from Your Terminal

Let's say you want to enter a definition       from your terminal,    but
the definition      won't all fit on one line.     The problem     is, if
you hit "return"     in the middle of a colon definition,      you will
leave   compilation      mode.   (Even if you don't     hit "return,"
!EXPECT! only accepts     eighty characters.)

How can you get          FORTH to resume coml?,..,ilation as you                  enter
subsequent lines?        By starting them with W· For example:


       BOXTEST 6 > ROT 22 > ROT 19 > AND ANDCl!lm) ok
         IF . " BIG ENOUGH" THEN ;mm, ok          --

(Some FORTH systems    stay in compilation     mode until    a uJis
encountered; on such systems the right bracket   is unnecessary.)
11 EXTENDINGTHE COMPILER                                                                    307




An Introduction        to FORTH Flowcharts


Flowcharts       provide   a way to visualize     the logical     structure     of a
definition,       to see where the branches      branch and where the loops
loop.       Old-fashioned      flowcharting      techniques      haven't       been
adequate      for describing    FORTH's structured    organization.        Instead,
various FORTH programmers have devised alternate               schemes.

The question   of which diagramming   approach   works best for FORTH
remains   open; programmers    use whatever    methods work best for
them.   The subject of flowcharting   could occupy a chapter    of its
own, but we're running out of chapters.

The diagrams     that we will use are loosely                    based on a type               of
flowchart   called    the "D-chart," invented                    by Prof. Edsger               W.
Dijkstra.  Here's how our diagrams work:

Sequential  statements           are written     one     below      the     other,   without
lines or boxes:


                             statement
                             next statement
                             next statement



Lines are used to show non-sequential   control                     paths      (conditional
branches  and loops). The FORTH statement

      condition    IF true     ELSE false      THEN statement

would be diagrammed



                                     condition


                          true
                                       ---,
                                         false

                              ~
                              statement



If either     phrase     is omitted,        a vertical       line         is drawn     in     its
place:
308                                                                       Starting   FORTH




                                      condition




                                 statement



It is immaterial    whether       "true"     is left   or right.


A IBEGINj.•• jUNTILI structure       is diagrammed         like   this:




The entire     loop structure        is shifted   to the right   from the
"normal"   flow of execution,        connected   by a horizontal    line at
the top.   If additional     levels    of nested  loops were to be shown,
they would be shifted    still    further to the right.

The black      dot is the symbol        for the end of the loop.          It
indicates   that control    is returned   to the return point, symbolized
by the circled     x. The condition will cause the loop either to be
repeated   or to be exited.      The diagonal    line sloping  down to the
left indicates    the return to the outer level of execution.
A !BEGINj.•. [wiITEE)
                   ... !REPEATI loop         is similar:
11 EXTENDING THE COMPILER                                            309




                              first   phrase




                                                 •
                                      second     phrase




We've given this brief   introduction    to FORTH flowcharts    so that
we can visualize the structure    of two very important  words.




Curtain    Calls



This   section      gives    us a
chance   to say "Goodbye"        to
the text interpreter      and the
colon   compiler     and perhaps
to see them in a new light.

Here is the definition      of
IINTERPRETI as it is found in
many FORTH systems (see page
216 for   a discussion     of
possible variations):
                                        ,,
                                             ,




          INTERPRET  BEGIN -' IF NUMBER ELSE EXECUTE
              ?STACK ABORT" STACK EMPTY" THEN O UNTIL


We've already     covered      each of the words contained       in this
definition;   we can describe         IINTERPRETI in English   by simply
"translating"  its definition,     like this:
310                                                                         Starting    FORTH




      Begin a loop.    Within the loop, try to look up the next word
      from the input stream.     If it's not defined,    try to convert it
      as a number.   If it is defined,    execute   it, then check to see
      whether  the stack     is empty.    (If it is, exit    the loop and
      print "STACK EMPTY.") Then repeat        the infinite    loop.

Now let's   apply   our flowcharting           techniques         to this     definition.



                      I IINTERPRETII
                                       until   end of line

                                                             _,

                                                    1
                                                    found


                                                     l
                                                  EXC.            NUMBER


                                       ABORT"




As you can see, the FORTH text     interpreter    is                          a simple  yet
powerful structure. Now let's compare its structure                            with that of
the colon compiler:



t For the Very Curious
You may have wondered,     if INTERPRET is an infinite  loop, how do
we exit   it and get back to QUIT?          The answer    varies for
different  implementations   of FORTH, but the most common answer is
this:
When you enter      a line   of text      from the terminal        and press
"return,"   the word IEXPECTI places        a "null"    (zero) at the end of
the input stream.    This null is actually       a defined     FORTH word; its
code field points directly      to JEXITI. The result:        when IINTERPRETJ
gets to the end of the line,       it finds null in the dictionary         and
executes  it.   )EXIT) immediately    transports     us up to IQUITI. Simple
and fast.
11 EXTENDING THE COMPILER                                                       311




              BEGIN -' IF (NUMBER) LITERAL
               ELSE ( check precedence bit) IF              EXECUTE ?STACK
                  ABORT" STACK EMPTY"
               ELSE 2- , THEN THEN O UNTIL


The first    thing    you probabl~    noticed       is that the name of the
colon compiler
after  creating
                    is not ill but
                   the dictionary
                                     W- The
                                       head
                                                 definition
                                                and performing
                                                              of [il invokes
                                                                   a few other
                                                                                   m
odd jobs.

The next        thing  you may have noticed            is that the      compiler  is
somewhat       similar  to the interpreter.           Let's translate     the above
definition       into English:


      Begin a loop.   Within the loop, try to look up the next word
      from the input stream.   If it's not defined, try to convert   it
      as a number t and, if it is a number, compile it as a literal.
      If it is defined,        then treat    it as a word.     If the word is
      immediate,     then execute      it and check to see if the stack is
      empty.      If it is not immediate,         change   the pfa to a cfa
      (code-field     address)     and compile   this address.    Then repeat
      the infinite     loop.


Picture      it this   way:   rn
                                     until   [ or ;




t For the Curious
The version    of INUMBERlthat the colon compiler     uses is the 16-bit
version.    That's why you can't  have a double-length      literal      in a
colon definition    (except by making it two single-length      literals).
312                                                            Starting   FORTH




Compare this to the diagram of IINTERPRETI and you'll see that []
could be called  an interpreter with the ability   to decide whether
to execute  or to compile any given word.    it is the simplicity  of
this design that lets you add new compiling    words so easily.

In summary, we've    shown two ways to extend        the FORTH compiler:

      1.   Add new, specialized        compilers,        by    creating     new
           defining words.

      2.   Extend    the existing   colon   compiler      by creating       new
           compiling    words.

While traditional     compilers    try to be universal  tools, the FORTH
compiler   is a collection      of separate,  simple tools ••• with room
for more. Which approach        seems more useful:


           COMPLEXITY                               OR   SIMPLICITY?


                                                   :~
                                                ~rA~          ....



                                            r rrr
11 EXTENDINGTHE COMPILER                                                 313




Here's   a summary of the words we've covered       in this   chapter:

  DOES>            run time:               Used in creating        a de-
                   ( -- adr)               fining word; marks the end
                                           of its compile-time    portion
                                           and the beginning       of its
                                           run-time portion.     The run-
                                           time operations    are stated
                                           in higher-level    FORTH. At
                                           run time, the pfa of the
                                           defined     word will be on
                                           the stack.
  IMMEDIATE         ( -        )           Marks the most recently
                                           defined word as one which,
                                           when encountered         during
                                           compilation,     will be exe-
                                           cuted     rather     than     be
                                           compiled.
  COMPILE xxx       ( -        )           Used in the definition      of a
                                           compiling    word.   When the
                                           compiling word, in turn, is
                                           used in a source       defini-
                                           tion,    the code field      ad-
                                           dress of xxx will be com-
                                           piled into the dictionary
                                           entry so that when the new
                                           definition   is executed, xxx
                                           will be executed.
  [COMPILE] xxx     ( -        )           Used in a colon definition,
                                           causes the immediate word
                                           xxx to be compiled          as
                                           though it were not imme-
                                           diate; XXX Will beexecuted
                                           when the definition          is
                                           executed.
  LITERAL           compile        time:   Used only inside        a colon
                    (n -       )           definition.        At compile
                    run time:              time,     compiles     a value
                    (   --n)               from the stack        into the
                                           definition    as a literal.    At
                                           run time, the value will be
                                           pushed onto the stack.
                                           Leaves compile mode.
                                           Enters   compile   mode.
314                                                         Starting   FORTH




Review of Terms

Compile-time
behavior             1.   when referring    to defining     words:     the
                     sequence of instructions     which will be carried
                     out when the defining     word is executed--these
                     instructions    perform the compilation       of the
                     member words;
                     2.    when referring    to compiling    words:    the
                     behavior of a compiling word, contained        within
                     a colon definition,    during compilation      of the
                     definition.
Compilee             a definition   being compiled.   In relation  to a
                     compiling word, the compilee is the definition
                     whose compilation   the compiling word affects.
Compiling     word   a word used inside a colon definition     to take
                     some action during the compilation  process.
Defining     word    a word which, when executed,         compiles   a new
                     dictionary    entry.    A defining    word specifies
                     the compile-time     and run - time behavior of each
                     member of the "family"            of words that      it
                     defines.
Flowcharts           a graphic      representation         of the logical
                     structure     of a program      or,    in FORTH, of a
                     definition.
Precedence     bit   in FORTH dictionary     entries,  a bit which
                     indicates  whether a word should be executed
                     rather than be compiled when it is encountered
                     during compilation.
Run-time
behavior             1. when referring        to defining    words:   the
                     sequence of instructions      which will be carried
                     out when any member word is executed;
                     2. when referring         to compiling    words:     a
                     routine    which will be executed         when the
                     compilee is executed.       Not all compiling words
                     have run - time behavior.
11 EXTENDING THE COMPILER                                                        315




Problems    -    Chapter     11


1.   Define  a defining word              named LOADED-BY that        will define
     words which load a block             when they are executed.       Example:

            6000 LOADED-BY CORRESPONDENCE

     would define      the word CORRESPONDENCE. When CORRESPONDENCE
     is executed,      block 6000 would get loaded.

2.   Define      a defining    word BASED. which   will           create   number
     output     words for specific  bases. For example,

            16 BASED. H.

     would define  H. to be a word which                prints   the top    of   the
     stack in hex but does not permanently              change   IBASEI.

            DECIMAL
            17 DUP H•• CIII!lmJ11 17 ok

3.   Define   a defining    word called  PLURAL which will take the
     address   of a word such as [£Bl or STAR and create    its plural
     form, such as CRS or STARS. You'll provide       PLURAL with the
     address    of the singular   word by using tick.   For instance,
     the phrase

            I   CR   PLURAL CRS

     will   define    CRS in the       same way as though     you had defined       it

            : CRS      ?DUP IF       O DO CR    LOOP THEN ;

4.   The French words for [QQIand LOOP are TOURNE and RETOURNE.
     Using the words [QQland LOOP, define   TOURNE and RETOURNE
     as French    "aliases." Now test them by writing yourself a
     French loop.
5.   The FORTH-79 Standard              Reference   Word Set contains      a word
     called     ASCII that    can       be used to make certain    definitions
     more readable.      Instead         of using a numeric ASCII code within
     a definition,    such as

            : STAR         42 EMIT ;

     you can use

            : STAR         ASCII *     EMIT ;

     The word ASCII reads the next character    in the input stream,
     then compiles  its ASCII equivalent   into the definition    as a
     literal.   When the definition    STAR is executed,     the ASCII
316                                                           Starting   FORTH




      value    is pushed   onto   the   stack.

      Define    the word ASCII.

6.    Write a word called   LOOPS which will cause the remainder     of
      the input stream,   up to the carriage  return, to be executed
      the number of times specified   by the value on the stack.   For
      example,

              7 LOOPS 42 EMIT       SPACECII1!Iil3*   * * * * * * ok
                                   12   THREE EXAMPLES


Programming in FORTH is more of an "art" than programming             in any
other   language.       Like painters       drawing   brushstrokes,   FORTH
programmers    have complete      control   over where they are going and
how they will get there.           Charles     Moore has written,   "A good
programmer    can do a fantastic        job with FORTH; a bad programmer
can do a disastrous         job."    A good FORTH programmer        must be
conscious   of "style."

FORTH style  is not easily taught; it's a subject that deserves                                            a
book of its own. Some elements of good FORTH style include:

      simplicity,

      the use of many short                definitions        rather         than     a few longer
      ones,

      a correspondence              between          words     and       easy-to-understand
      actions   or data        structures,

      well-chosen         names,     and

      well   laid-out      blocks,      clearly         commented.
One   good     way   to    learn     style,       aside     from     trial     and      error,       is   to
study existing  FORTH applications,      including     FORTH itself.  In
this book we've included    the definitions       of many FORTH system
words, and we encourage  you to continue      this study on your own.
This chapter introduces three                  applications           which         should       serve    as
examples of good FORTH style.
The first       example    will   show                  you the       typical          process    of
programming       in FORTH: starting                    out with     a problem          and working
step-by-step      towards the solution.
The second example involves         a more complex application        already
written:     you will see the use of well-factored        definitions      and
the creation    of an application-specific    "language."

The third    example               demonstrates      the way to translate       a
mathematical   equation             into a FORTH definition;     you will see how
speed and compactness                 can be increased     by using fixed-point
arithmetic.


                                                  317
318                                                              Starting   FORTH




(woiffil Game

The example      in this section       is a refinement      of the buzzphrase
generator    which we programmed back in Chap. 10. (You might want
to review     that    version     before   reading     this    section.)       The
previous   version    did not keep track of its own carriage             returns,
causing us to force !£sis into the definition            and creating      a very
ragged right margin.          The job of deciding      how many whole words
can fit on a line is a reasonable          application      for a computer and
not a trivial    one.

The problem     is this:     to draft     a "brief"   which consists     of four
paragraphs,       each    paragraph        consisting    of an appropriate
introduction     and sentence.        Each sentence      will consist    of four
randomly-chosen        phrases    linked     together  by fillers     to create
gramatically    logical    sentences     and a period at the end.

The words and phrases    have already     been edited   into blocks 234,
235, and 236 in the listing    at the end of this section.       Look at
these blocks now, without    looking   at the two blocks that follow
them (we're pretending   we haven't   written  the application   yet).

Block 234 contains  the four introductions.       They must be used in
sequence.   Block 235 contains   four sets of fillers.     The four sets
must be used in sequence,    but any of the three versions       within  a
set may be chosen     at random.     Block 236 contains       the three
columns of buzzwords from our previous      version,   with some added
words.

You might also look at          the     sample output     that     precedes    the
listing of the application,           to get a better    idea     of the desired
result.
"Top-down design"        is a widely accepted     approach   to programming
that can help to reduce development           time.    The idea is that you
first   study your application       as a whole, then break the problem
into smaller      processes,    then break these ' processes      into still
smaller    units.   Only when you know what all the units should do,
and how they will connect        together,  do you begin to write code.

The FORTH language        encourages     top-down design.      But in FORTH you
can actually       begin to write top-level        definitions     immediately.
Already       we can imagine         that    the  "ultimate      word"   in our
application      might be call€d      PAPER, and that it will probably          be
defined     something   like this:

      : PAPER     4 0 DO I INTRO SENTENCE LOOP ;
where INTRO uses the loop index as its argument     to select                  the
appropriate introduction. SENTENCE could be defined
      : SENTENCE      4 0 DO I FILLER       PHRASE LOOP ;
12 THREE EXAMPLES                                                          319




where FILLER uses the loop index as its argument to select       the
appropriate   set, then chooses at random one of the three versions
within    the set.   The function  of PHRASE will be the same as
before.
Using FORTH's editor,   we can enter these top-level definitions
into a block.   Of course we can't load the block until we have
written our lower-level  definitions.
In complicated     applications,        FORTH programmers      often test the
logic of their    top-level       definitions    by using "stubs"       for the
lower-level    words.     A stub is a temporary      definition.       It might
simply print a message to let us know its been executed.                   Or it
may do nothing at all, except resolve           the reference       to its name
in the high-level     definition.
While the top-down approach        helps to organize   the programming
process,     it isn't  always feasible    to code in purely    top-down
fashion.       Usually we have to find out how certain        low-level
mechanisms       will work before    we can design   the higher-level
definitions.
The best compromise is to keep a perspective     on the problem as a
whole while looking out for low-level     problems whose solutions
may affect the entire application.
In our example application,    we can see that it will no longer be
possible  to force [£Bis at predictable  points.  Instead we've got
to invent a mechanism whereby the computer will perform carriage
returns automatically.
The only way to solve this problem is to count every character
that is typed.    Before each word is typed, the application must
decide whether there is room to type it on the current line or do
a carriage  return first.

So let's define the variable LINECOUNTto keep the count and the
constant  RMARGIN with the value 78, to represent   the maximum
count per line.   Each time we type a word we will add its count
to LINECOUNT. Before typing      each word we will execute  this
phrase:
     (length   of next word) LINECOUNT@ + RMARGIN> IF CR
that is, if the length   of the next word added to the current
length   of the line exceeds   our right margin, then we '11 do a
carriage   return.

But we have another   problem: how do we isolate  words                 with   a
known count for each word? You got it, we use IWORDI.
Let's write    out        a "first  draft" of this low - level   part of our
application.         It    will type a single   word, making     appropriate
320                                                                 Starting      FORTH




calculations    for carriage      returns.


      32 WORD                                  Finds one      word delimited               by
                                               a space.

      COUNT DUP                                Leaves the count and a copy
                                               of the count    on the stack,
                                               with the address of the first
                                               character beneath.
      LINECOUNT @ +                            Computes      how long   the
                                               current  line would be if the
                                               word were to be included    on
                                               it.
      RMARGIN >                                Decides   if    it     would       exceed
                                               the margin.

      IF   CR O LINECOUNT                      If so, resets          the      carriage
                                               and the count.
      ELSE SPACE THEN                          Otherwise,  leaves               a space
                                               between the words.
      DUP l+ LINECOUNT +!                      Increases      the count by the
                                               length      of the word to be
                                               typed,      plus   one  for the
                                               space.
      TYPE                                     Types  the word using                   the
                                               count and the address                  left
                                               by COUNT.


Now the problem is getting   1 oR j to look at the strings                       on disk.
!WORD!gets its bearings               11
                         from BLK and j>INJ, so if we say,
      234 BLK !      0 >IN !t

then IWORDJwill       begin     scanning     block   234, starting          at the        top
(byte zero).




t For polyFORTH Users

The user variables    J>INJ and JBLKJ are adjacent  to each other in
the user table.    This design   allows you to fetch and store both
together with rafiland !rll- For example,
      234 0 >IN 2!
12 THREE EXAMPLES                                                                             321




This causes         another      problem:       by storing      new values        into the
input stream pointers,            we've destroyed        the old values.         If we now
execute        a definition          that   contains       the    above     phrase,      the
interpreter         will    not come back to us when it's                done;      it will
continue      trying     to interpret     the rest of block 234. To solve this
problem,       our definition         must save the pointer          values    somewhere
before      it changes       them, then restore         them just before        it's done.
Let's    define      a double-length         variable      called    HOMEBASE, so we
have a place         to save the pointers.           Then let's     write a word whose
job it will be to save the pointers                   in HOMEBASE. Finally,            let's
write a word which will restore               the pointers.


      VARIABLE HOMEBASE 2 ALLOT
        <WRITE BLK @ >IN @ HOMEBASE 2!
      : WRITE>  HOMEBASE 2@ >IN ! BLK !


Now we have to modify our highest-                   l evel definition slightly,                 by
editing in <WRITE at the beginning                   and WRITE> at the end:

      : PAPER       <WRITE 4 0 DO I INTRO SENTENCE LOOP WRITE> ;

The next question          is:   how do we know when             we've      gotten      to the
end of the string?

Since we are typing       word by word, we have to check whether         l>INI
has advanced   sixty-four     places  from its starting   point every time
we have found a new word.         But the limit is ' not always sixty-four
places;  in the case of the buzzwords, the limit is twenty places.

For this reason,  we should probably                 make the    limit     be an argument
to a word.   For example,  the phrase

      64 WORDS

should type out the          contents     of the 64-byte        string,     word by word,
performing carriage          returns     where necessary.

How should     we structure              our     definition       of      WORDS?         Let's
re - examine what it must do:

      1.     Determine     whether       there    is still    a word in the          string      to
             be typed.

      2.     If there     is, type       the word (with       margin      checking),          then
             repeat.     If there       isn't, exit.

The two part     nature    of this structure               suggests that we need a
IBEGINI... IWHILEl,.. JREPEATI loop.   Let's            write our problem this way,
if only to understand      it better.

      • • • BEGIN ANOTHER WHILE •WORD REPEAT •••
322                                                                    Starting      FORTH




ANOTHERwill         do step    li •WORDwill      do step     2.

How should ANOTHERdetermine    whether there is still                      a word to be
typed  from the string?    It must scan for the next                        word in the
block, by using the phrase

      32 WORD

then compare    the new value of l>INI against  the limit for l>IN!,
and finally  return a "true" if the value is less than or equal to
the limit.  This flag will serve as the argument for (w'iIIEE].

How do we compute the limit for !>IN!?    Before we can begin the
above loop, we have to add the argument (sixty-four     or whatever)
to the beginning  value of !>INI and save this limit on the stack
for ANOTHER to use each      time through     the loop.    Thus our
definition  of WORDSmight be

          WORDS ( u -- ) >IN @ + BEGIN ANOTHERWHILE
            • WORDREPEAT 2DROP i


We need the     DROP because, when we exit the 1oopj we will have
the address of WORD's buffer and the limit for 1>IN on the stack,
neither  of which we need any longer.

Now we can define ANOTHER. We've already     decided that the first
thing it must do is find the next word, by using the phrase
      32 WORD

At this    point,    there    will   be two values       on the stack:
      limit   adr

We can perform        the comparison        with the phrase
      OVER >IN @ < NOT

By using JOVER! we save the              limit   on the     stack    for   future    loops.
Remember that the phrase

      < NOT

is the same as "greater              than   .£E_ equal     to."     Our definition        of
ANOTHER, then, might be


      32 CONSTANTBL
        ANOTHER ( limit -- limit adr)
          BL WORD OVER >IN @ < NOT
12 THREE EXAMPLES                                                                323




(The abbreviation  BL is a common mnemonict         for     "blank."     We have
used it here to improve program readability.)

How do we define   • WORD? Actually,    we've      defined       it already,         a
few pages back, with the exception   that

      32 WORD

should be omitted  from the beginning  of the         definition,        since     it
will have been performed   in ANOTHER.

Now we have our word-typing         mechanism.      But let's   see if we 're
overlooking     anything.    For example,   consider    that every time we
start   a new paragraph,      we must remember to reset       LINECOUNT to
zero.    Otherwise our .WORD will think that the current          line is full
when it isn't.      We should ask ourselves      this question:       is there
ever a case in this application       where we would want to perform a
l£g] without resetting    LINECOUNT? The answer is no, by the very
nature of the application.       For this reason we can define
      : CR     CR O LINECOUNT ! :

to create       a version   of [£fil_that    is appropriate      for this
application.      We can use this!fBI   in our definition   of .WORD.
We should also consider        our handling    of spaces       between      words.
By using the phrase
      IF CR ELSE SPACE THEN

before typing each word, we guarantee       that there will be a space
between each pair of words on the same line but no space at the
beg inning of successive   lines.   And sine e we are typing    a space
before    each word rather     than  after,    we can place   a period
immediately   after a word, as we must at the end of a sentence.

But there's   still  a problem with this logic:  at the beginning    of
a new paragraph,      we will always get one s~tce before    the first
word.     Our solution:      to redefine iSPAC:[ so that  it will be
sensitive   to whether or not we're at the beginning   of a line, and
will not space if we ~=
      : SPACE      LINECOUNT @ IF SPACE THEN ;

If LINECOUNT is "0" then we know we are            at the      beg inning        of a
line, because of the way we have redefined          [£gl.


t -For Beginners

As a general  term, a "mnemonic"          is   a symbol     or abbreviation
chosen as an aid in remembering.
324                                                         Starting   FORTH




While we are redefining        SPACE, it would be logical    to include   the
phrase
      1 LINECOUNT+!
in the redefinition.   Again our reasoning   is that we should never
perform a space without incrementing       the count.    Now we can
eliminate   the word [±] from the definition      of .WORD, thereby
eliminating   a bug in the previous • WORD, namely that LINECOUNT
was getting incremented even at the beginning of the line.
Let's assume that we have edited our definitions    into a block.
(In fact, we've done this already in block 237.) Notice that we
had very little   typing  to do, compared    with the amount of
thinking we've done. FORTHsource tends to be concise.t
Now we can define our in-between-level   words--words    like INTRO
and PHRASE that we have already used in our highest-level     words,
but which we didn't define because we didn't have the low-level
mechanism.
Let's start   with INTRO.         First  we must set our input-stream
pointers.   The introductions      are all in block 234, so the phrase
      234 BLK !
takes care of them. Since each line is sixty-four      bytes long,         we
can calculate  the desired    offset into the block by mult~ing
the loop index by sixty-four,   then storing the offset into ~-
Now we're    ready to use WORDSto type all           the words in the next
sixty-four    bytes.  The finished definition           of INTRO looks like
this:
      : INTRO     ( u --    ) 64 * >IN !   234 BLK    CR 64 WORDS1
Our mechanism has given us a very easy way to select              strings.
Unfortunately     we cannot test this definition    by itself,  because it
does not reset the input-stream      pointers   to their original    values
when it's done. But we can get around this by writing ourselves a
definition    called TEST, as follows:
      : TEST CR '          <WRITE EXECUTEWRITE> SPACE
Now we can say



t For Experts
On the other hand, FORTH is not as compressed as APL, which in
our opinion is not nearly as readable as FORTH.
12 THREE EXAMPLES                                                                   325




        0 TEST INTRO
        IN THIS PAPER WE WILL DEMONSTRATETHAT ok
The "tick" in TEST will find the next word in the input stream,
INTRO, which will then be executed "between" <WRITE and WRITE>.
Notice that we put the argument to INTRO on the stack first.
The definition     for FILLER will be a little    more complicated.
Since we are dealing with sets, not lines, and since the sets are
four lines apart, we must multiply the loop index not by 64, but
by (64 * 4). To pick one of the 3 versions within the set, we must
choose a random number under three and multiply        it by 64, then
add this result     to the beginning    of the set.    Recalling    our
discussion   of compile-time arithmetic  in Chap. 11., we can define
         FILLER  ( u - ) [ 4 64 * ] LITERAL *
              3 CHOOSE 64 * + >IN ! 235 BLK                         64 WORDS
Again, we can test            this    definition       by writing
        3 TEST FILLER
        TO FUNCTIONAS ok
The remaining    words               in the application    are similar  to their
previous counterparts,               stated in terms of the new mechanism.
Here is a sample of the output, followed                       by our finished  listing.
(We've added block 239 as an afterthought                       so that we'd be able to
print    the   same   paper      more    than      once.)


IN THIS PAPER WE WILL DEMONSTRATE THAT BY APPLYING AVAILABLE
RESOURCES TOWARDS FUNCTIONAL DIGITAL CAPABILITY COORDINATED WITH
COMPATIBLE ORGANIZATIONAL UTILITIES IT IS POSSIBLE FOR EVEN THE
MOST RESPONSIVE DIGITAL OUTFLOW TO AVOID TRANSIENT UNILATERAL
MOBILITY.

ON THE ONE HAND, STUDIES HAVE SHOWN THAT WITH STRUCTURED DEPLOYMENT
Of TOTAL FAIL-SAFE MOBILITY BALANCED BY SYSTEMATIZED UNILATERAL
THROUGH-PUT IT BECOMES NOT UNfEASABLE FOR ALL BUT THE LEAST RANDOM
ORGANIZATIONAL PROJECTIONS TO AVOID RESPONSIVE LOGISTICAL CONCEPTS.

ON THE OTHER HAND, HOWEVER, PRACTICAL EXPERIENCE INDICATES THAT
WITH STRUCTURED DEPLOYMENT or QUALIFIED TRANSITIONAL MOBILITY
BALANCED BY REPRESENTATIVE LOGISTICAL THROUGH-PUT IT IS NECESSARY
FOR ALL REPRESENTATIVE UNILATERAL ENGINEERING TO FUNCTION AS
OPTIONAL DIGITAL SUPERSTRUCTURES.

IN SUMMARY, THEN, WE PROPOSE THAT WITH STRUCTURED DEPLOYMENT Of
RANDOMMANAGEMENTFLEXIBILITY BALANCED BY STAND-ALONE DIGITAL
CRITERIA IT IS NECESSARY FOR ALL QUALIFIED FAIL-SAFE OUTFLOW TO
AVOID PARTIAL UNDOCUMENTEDENGINEERING.
326                                                             Starting    FORTH




234   LIST

       0 IN THIS PAPER WE WILL DEMONSTRATE THAT
       1 ON THE ONE HAND, STUDIES HAVE SHOWN THAT
       2 ON THE OTHER HAND, HOWEVER, PRACTICAL EXPERIENCE INDICATES THAT
       3 IN SUMMARY, THEN, WE PROPOSE THAT
       4
       5
       6
       7
       8
       9
      10
      11
      12
      13
      14
      15


235 LIST

       0 BY USING
       1 BY APPLYING AVAILABLE RESOURCES TOWARDS
       2 WITH STRUCTURED DEPLOYMENT Or
       3
       4 COORDINATED WITH
       5 TO OrrSET
       6 BALANCED BY
       7
       8 IT IS POSSIBLE rOR EVEN THE MOST
       9 IT BECOMES NOT UNrEASABLE rOR ALL BUT THE LEAST
      10 IT IS NECESSARY rOR ALL
      11
      12 TO rUNCTION AS
      13 TO GENERATE A HIGH LEVEL Or
      14 TO AVOID
      15


236   LIST

       0    INTEGRATED          MANAGEMENT          CRITERIA
       1 TOTAL                  ORGANIZATIONAL      rLEXIBILITY
       2 SYSTEMATIZED           MONITORED           CAPABILITY
       3 PARALLEL               RECIPROCAL          MOBILITY
       4    rUNCTIONAL          DIGITAL             PROGRAMMING
       5 RESPONSIVE             LOGISTICAL          CONCEPTS
       6 OPTIMAL                TRANSITIONAL        TIME PHASING
       7 S YNCHRONIZED          INCREMENTAL         PROJECTIONS
       8 COMPATIBLE             THIRD GENERATION    HARDWARE
       9    QUALirIED           POLICY              THROUGH- PUT
      10    PARTIAL             DECISION            ENGINEERING
      11    STAND-ALONE         UNDOCUMENTED        OUTrLOW
      12    RANDOM              CONTEXT SENSITIVE   SUPERSTRUCTURES
      13    REPRESENTATIVE      rAIL - SArE         INTERACTION
      14    OPTIONAL            OMNIRANGE           CONGRUENCE
      15    TRANSIENT           UNILATERAL          UTILITIES


Copyrignt      rORTH,    Inc.   3/06/81   11:43      Starting       rORTH
12 THREE EXAMPLES                                                                    327




237 LIST

      0 C BUZZPHRASE GENERATOR II -- MARGIN SETTING )   EMPTY
      1 181 LOAD C RANDOMNUMBERS)
      2 32 CONSTANT BL           78 CONSTANT RMARGIN
      3 UARIABLE LINECOUNT       UARIABLE HOMEBASE 2 ALLOT
      4   <WRITE   BLK@   >IN@   HOMEBASE2!
      5   WRITE>   HOMEBASE2G >IN      BLK ! ;
      6
      7       CR    CR 0 LINECOUNT ! ;
      8       SPACE    LINECOUNT@ Ir SPACE 1 LINECOUNT +!      THEN
      9        .WORD   C adr ) COUNT DUP LINECOUNT@ + RMARGIN >
     10                Ir CR ELSE SPACE THEN
     11                DUP LINECOUNT + ! TYPE;
     12       ANOTHER C l i m - - l i m adr) BL WORD OUER >IN@ < NOT;
     13       WORDS ( U)
     14              >IN@+     BEGIN ANOTHER WHILE .WORD REPEAT 2DROP;
     15     238 LOAD     239 LOAD


238 LI ST
      0 ( BUZZPHRASE GENERATOR-- HIGH LEUEL WORDS>
      1
      2   BUZZ    16 CHOOSE 64 *+   >IN ! 236 BLK ! 20 WORDS
      3   1ADJ    0 BUZZ J
      4   2ADJ    20 BUZZ;
      5   NOUN 40 BUZZ;
      6   PHRASE    1ADJ 2ADJ NOUN
      7   rILLER    Cu)    [ 4 64 * J LITERAL*
      8        3 CHOOSE 64 *+>IN       235 BLK !    64 WORDS l
      9   SENTENCE    4 0 DO I rILLER PHRASE LOOP , " . " CR ;
     10   INTRO    ( ul    64 * )IN ! 234 BLK ! CR 64 WORDS;
     11
     12       PAPER    <WRITE   CR CR   4 0 DO I        INTRO SENTENCE LOOP WRITE>
     13
     14
     15       TEST    CR '   <WRITE EXECUTE WRITE> SPACE


239 LIST
      0       RETRIEUAL Or MORE SUCCESSrUL PAPERS )
      1
      2     UARIABLE SEED
      3
      4       4POSTERITY   RND @ SEED ! ;
      5       execute BErORE producing a paperl
      6
      7       REDO    SEED@ RND ! ;
      8       execute  ArTER a paper , to repr i nt       i t.
      9       Usage : REDO PAPER     >
     10
     11
     12
     13
     14
     15


Copyright      rORTH, Inc.        31'061'81   11 : 44            Sto1rting   rORTH
328                                                                           Starting         FORTH




File    Away!


Our second example consists       of a simple filing  system.t  It is a
powerful  and useful application,      and a good one to learn FORTH
style from. We have divided       this section into four parts:

        1.   A "How to" for the end user.  This will                         give     you an idea
             of what the application can do.

        2.   Notes on the way the                application         is structured          and the
             way certain definitions               work.

        3.    A glossary       of all      the definitions          in the    application.

        4.   A listing   of the           application,         including      the     blocks     that
             contain   the files           themselves.



How to Use the          Simple     File       System


This     computer      filing     system    lets   you store    and retrieve
information      quickly      and easily.     At the moment, it is set up to
handle     people's     names, occupations,        and phone numbers.!        Not
only does it allow you to enter,             change,  and remove records,       it
also allows you to search           the file for any piece of information.
For example,        if you have        a phone    number,   you can find      the
person's     name: or, given a name, you can find the person's               job,
etc.
For each person             there is a "record"   which contains   four                   "fields."
The names which             specify  each of these four fields   are

        SURNAME         GIVEN           JOB       PHONE

("Given,"       of course,       refers       to the     person's     given     name,      or first
name.)




tFor     Serious    File-Users

FORTH, Inc.        offers     a very      powerful     File    Management       Option.
+
+ For    Programmers

You can easily   change these                  categories        or extend          the   number      of
fields the system will handle.
12 THREE EXAMPLES                                                           329




File   Retrieval

You can search the file for the contents           of any field by using
the word FIND, followed by the field-name         and the contents, as in
       FIND JOB NEWSCASTERmI!lmJDAN RATHERok
If any "job" field contains    the string "NEWSCASTER," then the
system prints the person's  full name. If no such file exists, it
prints "NOT IN FILE."
Once you have found a field,     the record in which it was found
becomes "current."    You can get the contents of any field in the
current  record    by using the word GET. For instance,     having
entered the line above, you can now enter
       GET PHONEmI!lmJ555-9876   ok
The FIND command will only find the first instance  of the field
that you are looking   for.    To find out if there  is another
instance  of the field  that you last found, use the command
ANOTHER. For example,    to find another  person whose "job" is
"NEWSCASTER,"enter
                   JESSICA SAVITCH ok
       ANOTHERmI!lmJ

and
                     FRANK REYNOLDSok
       ANOTHERClll!llID
When there are no more people whose job is "NEWSCASTER" in the
file, the ANOTHERcommand will print "NO OTHER.II
To list all names whose field         contains   the   string   that   was last
found, use the command ALL:
       ALLlm!Jlm
       DAN RATHER
       JESSICA SAVITCH
       FRANK REYNOLDS
       ok
Since the surname and given name are stored separately,    you can
use FIND to search the file on the basis of either    one.   But if
you know the person's    full name, you can often save time by
locating   both fields  at once, by using the word FULLNAME.
FULLNAMEexpects the full name to be entered with the last name
first and the two names separated  by a comma, as in
       FULLNAMEWONDER,STEVIEmI!lmJSTEVIE WONDERok
330                                                             Starting   FORTH




(There must not be a space after    the comma, because    the comma
marks the end of the first field  and the beginning  of the second
field.)  Like FIND and ANOTHER, FULLNAME repeats       the name to
indicate  that it has been found.

You can actually  find any pair of fields   by using the word PAIR.
You must specify     both the field   names and their      contents,
separated  by a comma. For example,     to find a newscaster     whose
given name is Dan, enter

       PAIR JOB NEWSCASTER,GIVEN DANtm!Jml DAN RATHER ok



File   Maintenance


To enter a new record,   use the command ENTER, followed     by the
surname, given name, job, and phone, each separated    l;>y a comma
only.   For example,

       ENTER NUREYEV,RUDOLF,BALLETDANCER,555-1234tm!Jml ok

To change     the contents         of a single    field    within    the current
record,    use the command         CHANGE followed        by the    name of the
field,  then the new string.         For example,

       CHANGEJOB CHOREOGRAPHERtm!Jmlok

To completely        remove   the current   record,   use the command REMOVE:
       REMOVEtm!Jml ok

After adding,   changing, or removing records,   and before   turning
off the computer or changing   disks, be sure to use the word

       FLUSH ok



Comments

This section       is meant       as a guide,     for the   novice    FORTH
programmer,    to the glossary        and listing    which follow.      We'll
describe   the structure      of this application    and cover some of the
more complicated     definitions.     As you read this section,    study the
glossary   and listing     on your own, and try to understand        as much
as you can.
12 THREE EXAMPLES                                                                         331




Turn to the listing         now and look at block 242. This block
contains    the definitions     for all nine end-user commands we've
just discussed.   Notice how simple these definitions   are, compared
to their power!
This is a characteristic  of a well-designed   FORTH application.
Notice that the word -FIND, the elemental    file-search     word, is
factored in such a way that it can be used in the definitions      of
FIND, ANOTHER, and ALL, as well as in the internal      word, (PAIR),
which is used by PAIR and by FULLNAME.
We'll examine these          definitions   shortly,           but first      let's    look at
the overall structure        of this application.
One of the basic characteristics    of this application  is that each
of the four fields     has a name which we can enter in order to
specify the particular    field. For example, the phrase
      SURNAMEPUT
will put the character   string that follows in the input stream
into the "surname" field of the current record. The phrase
      SURNAME.FIELD
will print the        contents      of the       "surname"     field      of the      current
record , etc.
There are two pieces of information                    that are needed to identify
each field:    the field's   starting                    address    relative to the
beginning of a record and the length                    of the field.
In this     application,     a record        is laid   out like this:

  0                    16               28                              52                64
          surname
      .._.-,
                            given
                           --..---
                                                       job
                                                  .._.-,
                                                                              phone
                                                                          .._.-,
                                                                                           I
             16               12                         24                      12



For instance,        the "job" field starts twenty-eight    bytes in from
the beginning          of every record   and continues   for twenty-four
bytes.
We chose to make a record exactly   sixty-fo~tes      long so that
the fields will line up in columns when we l!d§!l the file.   This
was for our convenience  in programming, but this system could be
332                                                                Starting        FORTH




modified     to hold   records   of any length       and any number of fields.t

We've    taken the two pieces            of information
for    each     field       and put them          into   a
double-length         table    associated     with each
field      name.        Our definition           of JOB,
therefore,    is
                                                                    3         I    J
        CREATE JOB 28 , 24 ,                                        0        I     B
Thus when we enter the name of a field,       we                            link
are putting  on the stack the address     of the                        code pointer
table   that describes   the "job" field.     We
can   fetch    either   or both    pieces     of                            28
information  relative  to this address .                                    24

Let's call     each of these  entries a "field
specifying      table," or a "spec table"    for
short.




t For Those Who Want to Modify           This File     System

To change    the parameters     of the fields,   just make sure that the
beginning     byte {"tab")    for each field    is consistent    with the
lengths   of the fields   that precede    it . For example,   if the first
field is thirty   bytes long, as in
        CREATE lFIELD     O , 30 ,

then    make the tab for the second         field    thirty,    as in
        CREATE 2FIELD      30 , 12 ,

etc.    Finally,  set the value of R-LENGTH in line 4 to the length
of the entire    record  {the last field's    tab plus its length).  Using
R-LENGTH, the system automatically         computes the number of records
that can fit into a single block (1024 R-LENGTH /) and defines         the
constant    REC/BLK accordingly.

You may also change the location       of the new file (e.g., to create
several   different   files) by changing     the value of the constant
FILE in line 5. You may also change the maximum number of blocks
that your file can contain     by replacing    the "2" in the same line.
This value will be converted     into a maximum number of records,     by
being multiplied    by REC/BLK, and kept as the constant     MAXRECS.
12 THREE EXAMPLES                                                                333




Part   of the design  for this     application   is derived  from the
requirements  of FIND, ANOTHER, and ALL: that is, FIND not only
has to find a given string   within a given type of field,     but also
needs to "remember"     the string     and the type of field   so that
ANOTHER and ALL can search     for the same thing.

We can specify   the kind of field with just one value, the address
of the spec table for that type of field.     This means that we can
"remember"  the type of field by storing  this address  into KEEP.

KIND was created        for   this   purpose,    to   indicate    the   "kind"    of
field.

To remember the string, we have defined   a buffer called   WHAT to
which the string can be moved.   (WHAT is defined  relative  to the
pad, where memory can be reused,   so as not to waste dictionary
space.)

The word KEEP serves    the dual purpose   of storing     the given field
type into KIND and the given character       string   into WHAT. If you
look at the definition     of the end-user    word FIND, you will see
that the first  thing  it does is KEEP the information         on what is
being searched   for.  Then FIND executes     the internal    word -FIND,
which uses the information     in KIND and WHAT to find a matching
string.

ANOTHER and ALL also use -FIND, but they don't use KEEP. Instead
they look for fields that match the one most recently   "kept"  by
FIND.

So that    we can GET any piece     of information  from the record
which we have just "found,"     we need a pointer  to the "current"
record.      This need   is met with the variable     #RECORD.    The
operations      of the words TOP and DOWN in block 240 should       be
fairly   obvious to you.

The word RECORD uses #RECORD to compute            the absolute   address
(the computer-memory     address,     somewhere in a disk buffer)   of the
beginning   of the current    record.     Since RECORD executes   lBLOCKI,
it also guarantees   that the record really     is in a buffer.

Notice     that RECORD allows the file           to continue      over a range of
blocks.       !/MODI divides     the value     of #RECORD by the number of
records      per block    (sixteen    in this case,        since   each record    is
sixty-four      bytes long).      The quotient      indicates     which block the
record      will be in, relative        to the first       block:   the remainder
indicates      how far into that block this record will be.

While a spec table contains        the relative  address of the field and
its length,    we usually   need to know the field's       absolute  address
and length     for words such as JTYPEI, JMOVEI, and 1- TEXTJ. Look at
the definition      of the word FIELD to see how it converts               the
address     of a spec table     into an absolute     address     and length.
334                                                                   Starting     FORTH




Then examine          how FIELD is applied       in the definition          of .FIELD.

The word PUT also          employs    FIELD.     Its phrase

         PAD SWAP FIELD

leaves     on the stack      the arguments

         adr-of-PAD      absolute-adr-of-field         count

for IMOVEJto move the string                from the   pad     into   the   appropriate
field of the current record.

There are two things worth noting about the definition              of FREE in
block 241. The first       is the method used to determine           whether     a
record is empty.     We've made the assumption that if the first byte
of a record    is empty, then the whole record         is empty, because of
the way ENTER works.          If the first    byte contains       a character
whose ASCII value is less than thirty-three           (thirty-two     is blank),
then    it is not a printing        character     and the line       is empty.
(Sometimes an empty block will contain           all nulls, other times all
blanks; either    way, such records       will test as "empty.")        As soon
as an empty record      is found, LEAVE ends the loop.            #RECORD will
contain    the number of the free record.
Another   thing worth noting   about FREE is that it aborts  if the
file is full, that is, if it runs through  all the records  without
finding  one empty.   We can use a IQQ]loop to run through all the
records,   but how can we tell that the loop has run out before     it
has found an empty record?

The best way is to leave a "l" on the stack, to serve as a flag,
before  beginning  the loop.   If an empt~cord         is found, we can
change the flag to zero (with the word ~)         before we leave the
loop.   When we come out of the loop, we'll have a "l" if we never
found an emp~ record,     a "0" if we did.     This flag will be the
argument for ) ORT").

We use a similar    technique     in the definition     of -FIND. -FIND must
return a flag to the word that executed             it:  FIND, ANOTHER, ALL,
or (PAIR). The flag indicates          whether    a match was found before
the end of the file was reached.          Each of these outer words needs
to make a different       decision     based on the state       of this flag.
This flag is a II l" if a match is not found (hence the name -FIND).
The decision   to use negative       logic was based on the way -FIND is
used.

Because the flag needs to be a "1" if a match is not found, the
easiest   way to design   this word is to start     with a "l" on the
stack   and change   it to a "0" only if a match is found.        But
notice:    while the loop is running,    there  are two values on the
stack:   the flag we just mentioned   and the spec table address   for
the type of field    to be searched.      Since we need the address
12 THREE EXAMPLES                                               335




every time through the loop and the flag only once, if at all, we
have decided     to keep the address   on top of the stack and the
flag underneath.    For this reason, we use the phrase
       SWAP   NOT SWAP
By the way, we could have avoided the problem     of carrying   both
values on the stack by putting the phrase
       KIND @ FIELD
inside     the loop,   instead   of
       KIND@

at the beginning       and
         DUP FIELD
inside.    But we didn't, because we always try to keep the number
of instructions   inside a loop to a minimum. Naturally,  it is the
loops that take the most time running.
Now that you understand  the basic design of this application,  you
should have no trouble    understanding  the rest of the iisting,
using the glossary as a guide.t




tFor     polyFORTH Users
This type of glossary   is generated    by an application   called
DOCUMENTOR, which is inc l uded in the File Management Option.
336                                                                          Starting         FORTH




FORTH, Inc.                                                                 Page     1
                    SIMPLE FILES GLOSSARY
 WORD               VOCABULARY BLOCK STACK EFFECTS

 "RECORD        FORTH                     Z40       < -- adr)
     A variable   that points           to the    current  record.
 (PAIR)            FORTH            Z41       C adr)
     Starting      from the top, attempts       to find a match on the contents
     of WHAT, using KIND to indicate            the type of field.      If a match
      is made, then attempts      to match a second field,         whose type Is
      indicated      by adr, with the contents       of PAD. If both match,
     prints     the name; otherwise     repeats    until    a match is made or
     until    the end of the file     is reached,        in which case prints
      an error     message.
 -FIND          FORTH            Z41     ( -- f)
      Beginning   with #RECORD and proceeding    down, compares  the contents
      of the field    indicated by KIND against   the contents  of WHAT •
 . FIELD            FORTH             Z40        < adr>
      From the      current   record,   types the contents             of the   field       that   is
      associated       with the field-specifying        table         at adr.
 .NAME              FORTH                Z40
     From the       current   record,     types    the    name,    first   name first.
 ALL              FORTH            Z4Z
       Beginning   at the top of the file, uses KIND to determine   type                           of
       field   and finds  all matches on WHAT. Types the full   name<s>.
 ANOTHER       FORTH            Z4Z
    Beginning    with the next record      after   the             current  one, and using
    KIND to determine     type of . field,    attempts              to find a match on WHAT.
    If successful,    types the name; otherwise                    an error  message.
 CHANGE             FORTH            Z42
    Changes        the contents  of the given field               in the   current       record.
    usage:         CHANGE field-name     new-contents
 DOWN        FORTH                       240
    Moves the record          pointer     down one record.
 ENTER          FORTH          242
     Finds the first  free record,  then                 moves four strings   separated
     by commas into the surname,   given,                 job, and phone fields    of
     that record.
 FIELD           FORTH             240       C adr -- adr length)
     Given the address      of a field-specifying       table,    insures    that
     the associated    field   in the current     record     is in a disk buffer
     and returns    the address    of the field     in the buffer       along with
     its length.
 FILES         FORTH                     Z40        < -- ul
     The number of the         block     where    the files       begin.
12 THREE EXAMPLES                                                                                                       337




rORTH, Inc.                                                                              Page     2
                    SIMPLE rlLES GLOSSARY
 WORD               VOCABULARY BLOCK STACK ErrECTS
 f"IND           rORTH             242
      rinds   the record in which there      is a match                     between         the         contents
      of the given field     and the given str i ng.
          usage:    rlND field-name     string
 rREE                 rORTH              241
        Starting      at the top of the file,             finds the first                 record  that             is
        free,    that    is, whose first     byte        contains  a blank                or zero .
        Aborts     if the file    is full.
 rULLNAME      rORTH                     242
     rinds the record            in which there  is a match on both the                                 first      and
     last names given.              Usage:   rULLNAME lastname,firstname

 GET                 rORTH               242
        Prints    the contents      of the given          type        of field       from        the     current
        record.
 GIVEN               rORTH            240     C -- adr>
     Returns       the address  of the field-specifying                      table         for        the
     "given"       (first  name> field .
 .JOB               rORTH                240     c -- adr >
        Returns   the address       of the field - specify i ng table                      for        the
        "job" field.

 KEEP          rORTH              241       c adr >
     Moves a character    string,   delimited     either    by a comma or by a
     carriage  return,  from the input stream          into WHAT, and saves the
     address  of the given field-specifying          table   In KIND, for future
     use by -rIND .
 KIND           rORTH            240     C -- adr)
     A variable    that contains  the address  of the field-specifying
     table   for the type of field   that was last searched      for by rIND.
 MAXRECS     rORTH                       240                     U)
    The maximum number             of records       to    be allowed             in the     system.
 MISSING             rORTH              241
     Prints       the message      "NOT IN rILE."
 PAIR               rORTH              242
        rinds    the record   in which there      is a match between both the
        contents     of the first   given field      and the first  given string,  and
        and also the contents       of the second given field       and the second
        given string.       Comma is the delimiter.
            Usage:      PAIR f i eldl string1,field2        string2
 PHONE               rORTH               240      c -- adr>
     Returns       the address      of the field-specifying                      table     for         the
     "phone"       field.
338                                                                               Starting         FORTH




F"ORTH, Inc.                                                                      Page 3          3/06/81
                  SIMPLE F"ILES GLOSSARY
 WORD             VOCABULARY BLOCK STACK EF"F"ECTS
 PUT                 F"ORTH             241       < adr l
       Moves a character       string,     delimited    either   by a comma or by_ a
       carriage      return, from the input stream           into the field whose
       field-specifying      table     address    is given on the stack.
 R-LENGTH       F"ORTH              240             ( -- ul
     The length   in bytes      of a single          record.

 READ         F"ORTH            241
    Moves a character   string,   delimited either by a comma or by a
     carriage return, from the input stream into PAD.
 REC/BLK       F"ORTH                 240    ( --           u)
     The number of records         that Will fit            in a single           block,
     given MAXRECS.
 RECORD            F"ORTH          240     < -- adr)
     Insures     that the current   record  is in a disk buffer,                           and
     returns     the address  of the first   byte of that record.

 REMOVE            F"ORTH                242
    Erases      the current    record.
 SURNAME         F"ORTH          240      ( -- adr)
     Returns   the address  of the field-specifying                       table     for     the
     "surname"    (last name> field.
 TOP               F"ORTH                240
       Resets   the .record   pointer      to the     top        of the   file.
 WHAT         F"ORTH            240       -- adr)
    Returns  the address    of a buffer that contains    the string that
    is being searched    for, or was last searched    for, by F"IND.
12 THREE EXAMPLES                                                              339




240 LIST

      0   SIMPLE FILES>                                     EMPTY
      1                   ( tab length>                           ( tab length>
      2 CREATE SURNAME 0,             16,            CREATE GIVEN 16 ,     12 ,
      3 CREATE JOB          28,       24,            CREATE PHONE 52,      12,
      4 64 CONSTANT R-LENGTH                    1024 R-LENGTH / CONSTANT REC/BLK
      5 243 CONSTANT FILES                          2 REC/BLK * CONSTANT MAXRECS
      6 VARIABLE #RECORD                              VARIABLE KIND
      7   WHAT ( -- adrl           PAD 80 +;
      8   RECORD     C - - first      adr of current     record>
      9       #RECORD@ REC/BLK /MOD FILES+              BLOCK SWAP R-LENGTH * +
     10   FIELD     C field     --adr     length>    2@ RECORD+    SWAP;
     11    TOP    0 #RECORD ! ;
     12    DOWN 1 #RECORD+! ;
     13    .FIELD    ( field)       FIELD -TRAILING TYPE SPACE
     14    .NAME    GIVEN .FIELD           SURNAME .FIELD;
     15 241 LOAD 242 LOAD


241 LIST

      0     SIMPLE FILES, CONT'D>
      1     READ   44 TEXT ;
      2     PUT   C field>   READ PAD SWAP FIELD MOUE UPDATE
      3     KEEP   ( field)  DUP KIND !
      4                        2+@   READ PAD WHAT ROT MOVE
      5     FREE   1 MAXRECS 0 DO I #RECORD ! RECORD C@
      6       ( ASCII> 33 < IF NOT LEAVE THEN LOOP ABORT" FILE FULL'"
      7
      8     -FIND    C -- fl     1 KIND@    MAXRECS #RECORD@ DO
      9             I #RECORD!     DUP FIELD WHAT -TEXT NOT IF
     10                SWAP NOT SWAP LEAVE THEN LOOP DROP
     11     MISSING    .'" NOT IN FILE";
     12     (PAIR)    C field>      MAXRECS 0 DO I #RECORD!
     13       -FIND Ir    MISSING LEAVE ELSE DUP FIELD PAD -TEXT NOT
     14                          IF .NAME LEAVE THEN   THEN    LOOP DROP
     15


242 LIST
      0     SIMPLE FILES --    END USER WORDS>
      1
      2     ENTER    FREE   SURNAME PUT     GIVEN PUT
      3                     JOB PUT         PHONE PUT
      4     REMOVE    RECORD R-LENGTH 32 FILL   UPDATE;
      5     CHANGE       PUT
      6
      7     FIND       KEEP    TOP -FIND   IF MISSING ELSE .NAME THEN
      8     GET       .FIELD
      9
     10     ANOTHER DOWN-FIND    ff . '" NO OTHER '" ELSE . NAME THEN ;
     11     ALL  TOP BEGIN CR -FIND NOT WHILE .NAME DOWN REPEAT;
     12
     13     PAIR     KEEP    READ (PAIR) ;
     14     FULLNAME SURNAMEKEEP GIVEN READ <PAIR)
     15


Copyright    FORTH, Inc.         3/06/81   11: 44       Starting   FORTH
340                                                         Starting      FORTH




243   LIST

       0 FILLMORE           MILLARD     PRESIDENT                  NO PHONE
       1 LINCOLN            ABRAHAM     PRESIDENT                  NO PHONE
       2 BRONTE             EMILY       WRITER                     NO PHONE
       3 RATHER             DAN         NEWSCASTER                 555-9876
       4 FITZGERALD         ELLA        SINGER                     555-6789
       5 SAVITCH            .JESSICA    NEWSCASTER                 555-9653
       6 MCCARTNEY          PAUL        SONGWRITER                 555-1212
       7 WASHINGTON         GEORGE      PRESIDENT                  NO PHONE
       8 REYNOLDS           FRANK       NEWSCASTER                 555-0765
       9 SILLS              BEVERLY     OPERA STAR                 555-9876
      10 FORD               HENRY       CAPITALIST                 NO PHONE
      11 DEWHURST           COLEEN      ACTRESS                    555-9876
      12 WONDER             STEVIE      SONGWRITER                 555-0097
      13 FULi-ER            BUCKMINSTER WORLD ARCHITECT            555-7604
      14 RAWLES             .JOHN       PHILOSOPHER                555-9721
      15 TRUDEAU            GARRY       CARTOONIST                 555-9832


244   LIST

       0 VAN BUREN          ABIGAIL     COLUMNIST                  555-8743
       l ABZUG              BELLA       POLITICIAN                 555-4443
       2 THOMPSON           HUNTER s.   GONZO .JOURNALIST          555 - 9854
       3 SINATRA            FRANK       SINGER                     555-9412
       4 .JABBAR            KAREEM ABDULBASKETBALL PLAYER          555-4439
       5 MC GEE             TRAVIS      FICTITIOUS  DETECTIVE      555-8887
       6 DIDION             .JOAN       WRITER                     555-0009
       7 FRAZETTA           FRANK       ARTIST                     555 - 9991
       8 HENSON             .JIM        PUPPETEER                  555-0001
       9
      10
      11
      12
      13
      14
      15


245   LIST

       0
       l
       2
       3
       4
       5
       6
       7
       8
       9
      10
      11
      12
      13
      14
      15


Copyright    FORTH, Inc .       3/06/81   11: 44      St art i ng FORTH
12 THREEEXAMPLES                                                         341




No Weighting

Our final   example is a math problem which many people would
assume could only be solved by using floating               point.    It will
illustrate   how to handle     a fairly    complicated       equation    with
fixed-point      arithmetic    and demonstrate         that    for all the
advantages    of using fixed-point,     range and precision         need not
suffer.

In this example we will compute the weight of a cone-shaped    pile
of material,  knowing the height of the pile,      the angle of the
slope of the pile, and the density of the material.
To make the example more "concrete,"      let's weigh several huge
piles  of sand, gravel,   and cement.    The slope of each pile,
called  the "angle of repose,"  depends on the type of material.
For example, sand piles itself more steeply than gravel .


          .. .:
            -:--),.<:-42°
       ./~;. .
             :~-
              -..
               ~>....,
          sand                      cement

(In reality    these values vary widely, depending        on many factors;
we have chosen approximate      angles and densities       for purposes of
illustration.)
Here is the formula for computing the weight of a conical pile h
feet tall with an angle of repose of 6 degrees,    where D is the
density of the material in pounds per cubic foot:f

t For Skeptics
The volume of a cone, V, is given       by



where b is the radius of the base and h is the height.       We can
compute the base by knowing the angle or, more specifically,    the
tangent  of the angle.  The tangent  of an angle is simply the
ratio of the segment marked h to the segment marked bin        this
drawing:




                                                           (continued   ... )
342                                                                                   Starting     FORTH




      w
              3 tan      2   (0)


This will     be the formula                 which we must express                 in FORTH.

Let's design our application                         so that        we can    enter     the      name of a
material  first, such as

      DRY-SAND

then enter the height                  of a pile            and get   the
result for dry sand.

Let's     assume      th at for any one type          of
material       the density      and angle of repose
never     vary.       We can store     both of these
values      for each type of material           into     a                              CEMENT
table.        Since     we ultimately      need   each                                    131
angle's      tangent,    rather   than the number of
degrees,       we will store       the tangent.      For                                   700
instance,       the angle of repose for a pile of
cement       is 35°, for which the tangent             is
. 700. We will store this as the integer            700.
Bear in mind that our goal is not just to get an answer; we are
programming    a computer or device      to get the answer for us in the
fastest,   most efficient,      and most accurate   way possible.      As we
indicated     in Chap. 5, to write        equations   using   fixed-point
arithmetic   requires      an extra  amount of thought.     But the effort
pays off in two ways:




For Skeptics         (continued)

If we call        this       angle    11
                                           8 11 (theta),     then
                     h
      tan     e      b

Thus we can compute                  the radius            of the base      with
      b     = _h_
              tan        e
When we substitute   this  into the expression                                       for V, and then
multiply the result by the density D in pounds                                     per cubic foot, we
get the formula shown above.
12 THREE EXAMPLES                                                    343




     1.   vastly    improved   run-time  speed,  which can be very
          important when there are millions of steps involved in a
          single calculation,    or when we must perform thousands of
          calculations   every minute. Also,


     2.   program      size,    which
          would be critical          if,
          for instance,      we wanted
          to put this application
          in a hand-held        device
          specifically       designed
          as a pile-measuring
          calculator.        FORTH is
          often used in this type
          of instrument.


Let's approach    our problem by first considering    scale.   The
height of our piles ranges from 5 to 50 feet.   By working out our
equation   for a pile of cement 50 feet high, we find that the
weight will be nearly 35,000,000 pounds.
But because our piles will not be shaped as perfect           cones and
because our values are averages,      we cannot expect better       than
four or five decimal places of accuracy.t        If we scale our result
to tons, we get about 17,500. This value will comfortably             fit
within the range of a single-length          number.  For this reason,
let's   write    this    application entirely     with single - length
arithmetic    operators.
Applications  which require greater   accuracy can be written using
double-length   arithmetic;  to illustrate    we've even written     a
second version of this application      using 32-bit math, as you'll
see later on. But we intend to show the accuracy that FORTH can
achieve even with 16-bit math.
By running another test with a pile 40 feet high, we find that a
difference    of one-tenth    of a foot in height     can make a
difference of 25 tons in weight.  So we decide to scale our input
to feet and inches rather than merely to whole feet.




t For Math Experts:
In fact, since our height will be expressed       in three digits,   we
can't expect greater than three-digit  precision.     But for purposes
of our example, we'll keep better than four-digit    precision.
344                                                            Starting     FORTH




We'd like    the user   to be able   to enter

      15 FOOT 2 INCH PILE

where the words FOOT and INCH will convert   the feet and                   inches
into tenths of an inch, and PILE will do the calculation.                    Here's
how we might define FOOT and INCH:


        FOOT    10 * ;
        INCH    100 12 */ 5 + 10 / +

The use of INCH is optional.

(By the way, we could        as easily     have    designed    input      to be   in
tenths of an inch with      a decimal    point,   like this:

      15.2

In this case, NUMBER would convert     the input as a double-length
value.   Since we are only doing single-length       arithmetic,    PILE
could simply begin with !DROP!, to eliminate   the high-order    byte.)

In writing     the definition      of PILE, we must try to maintain         the
maximum number of places           of precision      without    overflowing   15
bits.   According      to the formula,       the first    thing   we must do is
cube the argument.           But let's    remember     that   we will have an
argument which may be as high as 50 feet, which will be 500 as a
scaled    integer.      Even to square         500 produces     250,000, which
exceeds    the capacity     of single - length arithmetic.
We might reason  that,  sooner or later   in this calculation,               we're
going to have to divide   by 2000 to yield an answer in tons.                 Thus
the phrase

      DUP DUP 2000 */

will square the argument and convert      it to tons at the same time,
taking   advantage   of EZ]'s double-length      intermediate  result.
Using 500 as our test argument, the above phrase will yield 125 . .

But our pile may be as small as 5 feet, which when squared is only
25. To divide  by 2000 would produce a zero in integer  arithmetic,
which suggests that we are scaling  down too much.
To retain   maximum accuracy,     we should scale         down no more than
necessary.   250,000 can be safely    accommodated         by dividing by 10.
Thus we will begin our definition     of PLLE with        the phrase

      DUP DUP 10 */

The integer  result  at this stage will be scaled              to one place       to
the right of the decimal point (25000 for 2500.0).
12 THREE EXAMPLES                                                                          345




Now we must cube         the  argument.         Once       again,     straight
multiplication  will produce a double-length           result,    so we must use
E{1 to scale down. We find that by using 1000 as our divisor, we
can stay just within single-length      range.     Our result at this stage
will be scaled     to one place    to the left        of the decimal        point
{12500 for 125000.) and still  accurate    toSdigits.

According     to our formula,         we must multiply our argument               by pi.    We
know that     we can do this         in FORTH with the phrase

        355 113 */

We must also divide            our argument     by 3.     We can         do both     at once
with the phrase

        355 339 */

which    causes      no problems     with scaling.

Next we must divide our argument by the tangent       squared, which we
can do by dividing     the argument   by the tangent    twice.  Because
our tangent    is scaled    to 3 decimal   places,   to divide   by the
tangent  we multiply    by 1000 and divide   by the table value.    Thus
we will use the phrase

        1000 THETA @ */

Since   we must perform    this twice,    let's  make it a definition,
called   /TAN {for divide-by-the-tangen~         and use the word /TAN
twice in our definition      of PILE.    Our result  at this point     will
still  be scaled to one place to the left of the decimal       (26711 for
267110, using our maximum test values).

All that remains is to multiply    by the density  of the material,    of
which    the highest     is 131 pounds   per cubic   foot.    To avoid
overflowing,    let's try scaling   down by two decimal    places   with
the phrase
        DENSITY@ 100 */

But by testing, we find that the result  at this point for a SO-foot
pile of cement will be 34,991, which just exceeds   the 15-bit limit.
Now is a good time to take the 2000 into account.     Instead of

        DENSITY@ 100 */

we can say

        DENSITY@ 200 */

and our answer         will    now be scaled    to whole        tons.
You will      find      this    version    in   the   listing       of    block     246 that
346                                                              Starting    FORTH




follows.   As we mentioned,     we have also written      this application
using double-length    arithmetic,    in block 248. In this version        you
enter the height    as a double-length      number scaled     to tenths  of a
foot, followed by the word FEET, as in 50.0 feet.
By using double-length          integer    arithmetic,     we are able to compute
the weight of the pile to the nearest                whole pound.      The range of
double-length        integer      arithmetic      compares      with that     of most
floating-point       arithmetic.        Below is a comparison        of the results
obtained       using   a 10-decimal-digit           calculator,     single-length
FORTH, and double-length            FORTH. The test assumes a 50-foot pile
of cement, using the table values.


                                   in pounds
                                                           ---
                                                           in tons

            calculator             34,995,634              17,497.817
            FORTH 16-bit                                   17,495
            FORTH 32-bit           34,995,634              17,497.817


Here's   a sample   of our application's        output:

      246 LOAD ok
      CEMENT o'i<"
      10 FOOT PILE = 138 TONS OF CEMENT ok
      10 FOOT 3 INCH PILE = 151 TONS OF CEMENT ok
      DRY-SAND ok
      10 FOOT PILE = 81 TONS OF DRY SAND ok
      248 LOAD CEMENT ok
      10.0 FEET = 2799W-POUNDS OF CEMENT OR 139.969 TONS ok


A note   on"

The defining     word MATERIAL takes    three   arguments   for each
material,   one of which is the address    of a string.   .SUBSTANCE
uses this address to type the name of the material.

To put the string       in the dictionary       and to give an address      to
MATERIAL, we have defined         a word called      ". As you can see from
its definition,       "compiles      the string    {delimited    by a second
quotation    mark, ASCII 34) into the dictionary,           with the count in
the first byte, and leaves       its address     on the stack for MATERIAL.
To compile      the count and strin       into the dictionary,      we simply
have to execute      !WORD!,since, , WORD's buffer is !HERE!. We get the
string's  address as a fillip,      since WORD also leaves !HERE!.

All that remains   is to !ALLOT! the appropriate   number of bytes.
This number is obtained   by fetching the count from the first byte
of the string and adding one for the count's byte.
12 THREE EXAMPLES                                                               347




246 LIST

      0 ( WEIGHT OF CONICAL PILES -- SINGLE-LENGTH)      EMPTY
      1 VARIABLE DENSITY   VARIABLE THETA    VARIABLE STRING
      2 34 CONSTANT QUOTE
      3       QUOTE WORD DUP CG 1+ ALLOT
      4   .SUBSTANCE   STRING@   COUNT TYPE SPACE;
      5
      6      MATERIAL  ( STRING DENSITY THETA) CREATE , , ,
      7        DOES> DUP@ THETA!    2+ DUP@ DENSITY ! 2+ G STRING
      8
      9      FOOT    10 * J
     10      INCH    100 12 */    5 + 10 /    +
     11
     12   /TAN   1000 THETA G */;
     13   PILE   DUP DUP . 10 */ 1000        */      355 339 *//TAN/TAN
     14         DENSITY@ 200 */                :            "TONS OF" .SUBSTANCE
     15 247 LOAD


247 LIST
      0   TABLE OF MATERIALS>
      1 < STRING-ADDRESS  DENSITY            THETA>
      2"  CEMENT"            131               700     MATERIAL CEMENT
      3"  LOOSE GRAUEL"       93               649     MATERIAL LOOSE-GRAUEL
      4"  PACKED GRAVEL"     100               700     MATERIAL PACKED-GRAUEL
      5"  DRY SAND"           90               754     MATERIAL DRY-SAND
      6 " WET SAND"          118               900     MATERIAL WET-SAND
      7 " CLAY"              120               727     MATERIAL CLAY
      8
      9
     10
     11
     12
     13
     14 CEMENT
     15


248 LIST
      0 C WEIGHT OF CONICAL PILES  -- DOUBLE-LENGTH)     EMPTY
      1 VARIABLE DENSITY    VARIABLE THETA   VARIABLE STRING
      2 34 CONSTANT QUOTE
      3 • "    QUOTE WORD DUP C@ 1+ ALLOT
      4   .SUBSTANCE    STRING G COUNT TYPE SPACE;
      s   U.3    <a a a a 46 HOLD as a> TYPE SPACE
      6   MATERIAL    ( STRING DENSITY THETAl CREATE
      7       DOES> DUP@ THETA ! 2+ DUP@ DENSITY       2+@ STRING
      8
      9       CUBE      d    dl   2DUP OVER 10 M*/ DROP 10 M*/
     10       /TAN      d    dl   1000 THETA@ M*/
     11       FEET     d     dl    CUBE 355 339 M*/ DENSITY@ 1 M*/
     12                  /TAN /TAN 5 M+ 1 10 M*/
     13               2DUP     " - " D. . " POUNDS Or " . SUBSTANCE
     14             1 2 M*/      "OR"   U.3    "TONS"
     15     247 LOAD


Copyright      FORTH, Inc.        3/06/81     11: 45        Starting   FORTH
348                                                    Starting   FORTH




Review of Terms


Stub              in FORTH, a temporary          definition    created
                  solely      to allow testing     of a higher-level
                  definition.
Top-down
programming       a programming    methodology      by which a large
                  application    is divided     into smaller     units,
                  which may be further subdivided        as necessary.
                  The design process starts with the overview, or
                  "top," and proceeds     down to the lowest level
                  of detail.    Coding     of the low-level       units
                  begins only after the entire       structure   of the
                  application  has been designed.
                                          APPENDIX                1
                                       ANSWERSTO PROBLEMS


Chapter       1

1.        GIFT    • II      BOOKENDS II ;
          GIVER        • II    STEPHANIE II
          THANKS          • II  DEAR II GIVER            II   ,       THANKS FOR THE       II

             GIFT                 II •,




2.        TEN-LESS            -10 +       or
          TEN-LESS            10 - ;

3.    When      THANKS     was compiled,     the  definition                               included     a
      reference      to the first    version  of GIFT (the                            only   version   of
      GIFT at that      time).   Thus THANKS will   always                           execute     the same
      version     of GIFT.


Chapter       2


1.    DUP DUP:              (1 2 -- 1 2 2 2)
      2DUP:                (1 2 -- 1 2 1 2)

2.    SWAP 2SWAP SWAP

3.        3DUP         DUP 2OVER ROT

4.        2-4        OVER    + * + ;
5.        2-5        2DUP -     ROT ROT + /         ;
6.        CONVICTED-OF             0 ;                                HOMICIDE    20 + ;
          WILL-SERVE                II YEARS   II                     ARSON    10 + ;
                                                                      BOOKMAKING      2 + ,
                                                                      TAX-EVASION      5 + ;

7.        EGG.CARTONS     12 /MOD                   II   CARTONS AND            II

                II LEFTOVERS II ;


Chapter         4

1.    1 0= NOT • 1 ok
      0 0= NOT • 0 ok
      200 0= NOT---:-rok

2.    Don't         ask.




                                                1-1
1-2         Answers                                                     Starting       FORTH




3.    (assuming         the   legal     age   is 18 or over:)

           CARD .     17 > IF • " ALCOHOLIC BEVERAGES PERMITTED                    "
                        ELSE • " UNDER AGE " THEN ;

4.         SIGN. TEST         DUP 0=       IF • " ZERO " ELSE
                              DUP 0<       IF • " NEGATIVE " ELSE
                                             ."POSITIVE"   THEN THEN DROP
      (or    anything         else    that works)

5.         STARS        ?DUP         IF STARS THEN

6.      <ROT    ROT ROT ;
      : WITHIN    <ROT OVER > NOT <ROT > AND ;
      Or here's  a more efficient version, using tricks                    introduced          in
      the next chapter:
        WITHIN    >R 1- OVER < SWAP R> < AND ;

7.         GUESS ( answer guess - answer          or  -  )
              2DUP = IF • " CORRECT! " 2DROP ELSE
              2DUP < IF • n TOO HIGH II ELSE • 11 TOO LOW •
                                             THEN DROP THEN

8.         SPELLER            DUP ABS 4 > IF • "OUT OF RANGE " ELSE
                              DUP 0< IF • " NEGATIVE " ABS THEN
                              DUP 0= IF • " ZERO " ELSE
                              DUP 1 = IF ." ONE " ELSE
                              DUP 2 = IF ." TWO " ELSE
                              DUP 3 = IF • " THREE " ELSE
                                           11
                                         •    FOUR "
                              THEN THEN THEN THEN THEN DROP

9.    assuming   <ROT and WITHIN are still       loaded:
         3DUP    DUP 2OVER ROT;
         TRAP     ( answer   low-try hi-try   -- answer                          or
          3DUP OVER=       <ROT= AND IF ." YOU GOT IT!                        "DROP      ELSE
          3DUP SWAP l + SWAP WITHIN IF."           BETWEEN"
              ELSE."    NOT BETWEEN"     THEN THEN 2DROP;


Chapter      5

1.    */ MINUS                                          4.      F>C    32 - 10 18 */ ;
                                                                C> F   18 10 */ 32 + ;
2.    MAX MAX MAX •                                             K>C    273 - ;
                                                                C>K    273 + ;
3.    a)     0 32 - 10 18 */ . -17 ok                           F>K    F>C C>K
      b)     212 32 - 10 18 */ . 100 ok                         K>F    K>C C>F
      c)     -32 32 - 10 18 */ . -35 ok
      d)     16 18 10 */ 32 + . 60 ok
      e)     233 273 - • - 40 ok
APPENDIX 1                                                                Answers         1-3




186 LIST

      0     ANSWERS, CHAP, 6)                EMPTY
      1     PROBLEMS 1 - 6)
      2     STARS    0 DO,"*"       LOOP
      3     BOX    0 DO CR DUP STARS LOOP DROP
      4     ,sTARS    < #-of-lines>      0 DO CR I SPACES   10 STARS LOOP
      5     /STARS    ( #-of-lines)      1 SWAP DO CR I SPACES 10 STARS
      6                      -1 +LOOP I
      7     ( USING BEGIN & UNTIL FOR /STARS:)
      8     A/STARS    < #-of-lines>      BEGIN CR DUP SPACES 10 STARS
      9          1- DUP 0: UNTIL DROP;
     10
     11     DIAMONDS DEFINED IN TWO STAGES:)
     12     TRIANGLE DO CR 9 I - SPACES
     13              I 2* 1+ STARS DUP +LOOP DROP;
     14     DIAMONDS 0 DO 1 10 0 TRIANGLE
     15                     -1 0 9 TRIANGLE LOOP;

187 LIST

      0     ANSWERS, CHAP. 6,      CONT'D)             EMPTY
      1
      2     PROB. 7>
      3     RX   10 */ 5 + 10 / I
      4     DOUBLED    < AMT INT -- )
      5          OVER 2* ROT ROT SWAP 21 1 DO
      6               CR."   YEAR"    I 2 U.R 3 SPACES
      7                        2DUP RX+ DUP ,"BAL    "
      8                  DUP 2OVER DROP> Ir
      9           CR CR " MORE THAN DOUBLED IN " I . , " YEARS " LEAVE
     10                                        THEN LOOP 2DROP DROP;
     11
     12     PROB. 8)
     13     **   1- ?DUP Ir
     14         OVER ROT ROT       0 DO OVER*     LOOP SWAP DROP THEN
     15


188 LIST

      0     ANSWERS, CHAP. 7)                         EMPTY
      1     PROB. 1)
      2     N-MAX      0 BEGIN 1+ DUP 0( UNTIL 1-
      3     Keeps incrementing         the number on the stack        by one until
      4     it looks negative,         Which means the limit       has been passed.
      5     The final    1- sets     it back to what it was just          before   it
      6     surpassed    the limit.)
      7     PROB. 2 -- Assume that          HUMOROUSand SENSITIVE are
      8       both true . The "anded"          result     is "'1", How assu111e
      9       that   ART-LOVING and MUSIC-LOVING are also both true ,
     10       If we "+" their     flags     instead     of "OR"ing theft!, we get "2. "
     11                     But 0001 ronel
     12            ANDed with 0010 rtwol
     13                  gives   0000, wh i ch is false.>
     14
     15


Copyright    FORTH, Inc .          31'061'81   11:40           Starting   FORTH
1-4         Answers                                                              Starting       FORTH




189 LIST

       0        ANSWERS, CHAP. 7     CONT'DJ    El1PTY
       1
       2
                PROB. 3)
                BEEP      ..BEEP"  7 EMIT ;
       3        DELAY    20000 0 DO LOOP ;
       4        3BELLS    BEEP DELAY BEEP DELAY BEEP
       5
       6        PROB.   4-a>
       7        F>C     -320 11+ 10 18 11*/ ;
       8        C)F     18 10 l'I*/ 320 M+ ;
       9        K>C     -2732 M+ ;
      10        C>K       2732 M+ ;
      11        F>K     F >C C>K
      12        K>F     K >C C>F ;
      13        PROB.   4-b)
      14        . DEG     SWAP OVER DABS
      15          <ti   ti 46 HOLD tiS SIGN ti)          TYPE SPACE


190 LIST

       0        ANSWERS, CHAP. 7 -- CONT'D>
       1    C   PROB. 5)
       2        DPOLY    ( x -- dv>
       3              DUP 7 l'I*   20 M+ ROT 1 l'I*/   5 11+;
       4        ?DMAX 0 BEGIN         1+ DUP DPOLY 0 0 D< UNTIL 1-.
       5          ?DMAX .1ret/   17513 ok    -- this takes    a while)
       6
       7
       8        PROB. 6)
       9        BINARY 2 BASE !
      10        3-BASES
      11           17 0 DO CR "DECIMAL"                DECIMAL   I 4 U.R 8 SPACES
      12                      " HEX "                  HEX       I 3 U.R 8 SPACES
      13                      '' BINAl'!Y"             BINARY    I 8 U.R  8 SPACES
      14                                                             LOOP DECIMAL;
      15


191 LIST

       0        ANSWERS, CHAP. 7 -- CONT'D)
       1        PROB. 7 -- It tells    you that    double-length      routines              are
       2        loaded.   Two dots  are interpreted        as a double-length                zero.>
       3
       4        PROB. BJ
       5        .PHI*  <ti     ti ti ti ti45 HOLD ti ti ti
       6                       OVER IF 47 HOLD tis THEN '*>TYPE SPACE;
       7        OVER supplies     IF with the low-order     cell    of the
       8        number being    converted   .  This cell   contains    zero only
       9        when conversion     has completely    "used up" the number.)
      10
      11
      12
      13
      14
      15


Copyright        FORTH, Inc.                 3/06/81   11:40          Starting     FORTH
APPENDIX 1                                                                   Answers        1-5




192 LIST

      0       ANSWERS, CHAP. 8)                    EMPTY
      1       PROB. 1-a)
      2     VARIABLE PIES      0 PIES !
      3       BAKE-PIE     1 PIES +!
      4       EAT-PIE     PIES(?    IF -1 PIES+!      " THANK YOU "
      5                             ELSE ." WHAT PIE? "THEN ;
      6     ( PROB 1-b)
      7     VARIABLE FROZEN-PIES         0 FROZEN- PIES
      8       FREEZE-PIES      PIES (? FROZEN-PIES+!         '
                                                          0 PIES I
      9     ( PROB. 2)
     10       .BASE     BASE (? DUP DECIMAL       BASE !
     11     ( PROB. 3)
     12     VARIABLE PLACES       0 PLACES !
     13     : M.    SWAP OVER DABS <II
     14             PLACES@ ?DUP IF       0 DO II   LOOP 46 HOLD THEN
     15                                      IIS SIGN II> TYPE SPACE;


193 LIST

      0   ANSWERS, CHAP. 8 -- CONT'D)                     EMPTY
      1
      2   Prob. 4)
      3 VARIABLE IIPENCILS 6 ALLOT
      4 0 CONSTANT RED                             2 CONSTANT BLUE
      5 4 CONSTANT GREEN                           6 CONSTANT ORANGE
      6
      7         PENCILS    !!PENCILS+
      8
      9 23 RED PENCILS !
     10 15 BLUE PENCILS!
     11 12 GREEN PENCILS!
     12 0 ORANGE PENCILS!
     13
     14 ( To test,        we can enter
     15               BLUE PENCILS?      15 Ok
                                                                              194 LOAD
                                                                              PLOT
194 LIST                                                                       0
                                                                               1   *
      0         ANSWERS, CHAP. 8,     CONT'D)     EMPTY                        2   **
      1                                                                        3 ***
      2   PROB. 5)
            (                                                                  4 ****
      3 CREATE 'SAMPLES         20 ALLOT       10 CELLS)                       5 *****
      4   STARS      ?DUP IF 0 DO 42 EMIT LOOP THEN                            6 ******
      5   SAMPLES      ( indexll   - - adr  )   2* 'SAMPLES+                   7
      6   IN IT-S AMPLES            --
                                     )                                          8 *
                                                                                9 **
      7         11 0  DO   I 7   MOD   I  SAMPLES ! LOOP ;
      8                                                                        10 ***
      9         PLOT   (
     10            11 0 DO     CR   I 2 U.R     SPACE   I SAMPLES(?         STARS LOOP CR
     11
     12 !NIT-SAMPLES
     13
     14
     15


Copyright        FORTH, Inc.                                     Starting     FORTH
1-6         Answers                                                               Starting   FORTH




195 LIST

       0   ANSWERS, CHAP. 8)         EMPTY
       1   PROB. 6)
       2 UARIABLE BOARD 7 ALLOT
       3   CLEAR     BOARD 10 0 FILL        CLEAR
       4   SQR     BOARD+;
       5   BAR         ,   ,
       6   DASHES      CR 9 0 DO "-"    LOOP CR;
       7   .BOX     SQR ce DUP 0= IF 2 SPACES ELSE
       8                  DUP 1 = IF  " X"    ELSE
       9                              "0"     THEN THEN DROP;
      10   DISPLAY       CR 9 0 DO
      11      I IF   I 3 MOD 0= IF DASHES ELSE BAR THEN THEN
      12          I .BOX LOOP CR QUIT;
      13   PLAY     1-   0 MAX 8 MIN SQR C! ;
      14   X!     1 SWAP PLAY DISPLAY
      15   O! - 1 SWAP PLAY DISPLAY;


196   LIST

       0        ANSWERS, CH. 9)                                   EMPTY
       1        PROB. 1)
       z        COUNTS     ROT ROT 0 DO             OUER EXECUTE LOOP            SWAP DROP
       3
       4        PROB. 2)
       5        You can find out      by entering
       6           EMPTY HERE.                           )
       7
       8        PROB. 3)
       9        You can find out      by entering
      10           PAD HERE -                            )
      11
      12        PROB. 4)
      13    (   a. Ho ciiff~rence.        A VARIABLE returns         its own pfa.
      14        b. A user variable        returns      ttle address    of a cell   in ttle user
      15        table.    Ttle dictionary       entry,     wtlictl • finds,   is elsewnere.l


197 LIST
       0   ANSWERS, CHAP. 9, CONT'D)
       1 < PROB. 5, SOLUTION ~1)
       2 VARIABLE 'TO-DO    10 ALLOT ( 6 CELLS)
       3   TO-DO    ( index -- adrl  1- 2•   'TO-DO +
       4
       5        GREET   . " HELLO, I SPEAK FORTH. " ;
       6        SEQUENCE     11 1 DO I . LOOP;
       7        TILE   10 5 BOX;     < see answers, en.               6)
       8        NOTHING
       9
      10'  GREET             1 TO-DO !               ' SEQUENCE 2 TO-DO I
      11 ' TILE              3 TO-DO                 ' NOTHING  4 TO-DO!
      12 'NOTHING            5 TO-DO                 ' NOTHING  6 TO-DO
      13
      14        DO-SOMETHING        ( index    --    >       TO-DO@   EXECUTE
      15


Copyright        FORTH, Inr..                                         Starting      FORTH
APPENDIX 1                                                           Answers   1-7




198 LIST

      0   ANSWERS, CHAP. 9, CONT'D)
      1   PROB. 5, SOLUTION nz)
      2 VARIABLE 'TO-DO    10 ALLOT   6 CELLS)
      3   TO-DO    C index -- adr)  1- 2*   'TO-DO+
      4
      5     GREET   ." HELLO, I SPEAK FORTH.
      6     SEQUENCE    11 1 DO I . LOOP;
      7     TILE   10 5 BOX;    c see answers,      Ch.   6>
      8     NOTHING l
      9
     10    INIT"TO - DO" < -- ) 7 1 DO ['J  NOTHING I TO-DO ! LOOP
     11     [ 'l GREET 1 TO-DO!       C'l SEQUENCE 2 TO-DO !
     12     ['J  TILE   3 TO-DO
     13 INIT"TO-DO"
     14
     15:  DO-SOMETHING     < index -- ) TO-DO@    EXECUTE


199 LIST

      0     ANSWERS, CHAP. 10)                 EMPTY
      1
      2     PROB. 1)
      3     CHANGE < c1 c2 -- >  < changes  c1 to c2>
      4      SWAP 228 BLOCK 1024 OVER+ SWAP DO
      5                 2DUP IC@  : IF IC!    ELSE DROP THEN
      6                                 LOOP 2DROP
      7
      8  ( PROB. 2)
      9 181 LORD ( RANDOMNUMBERS>
     10:   FORTUNE    CR 16 CHOOSE 64 * < blockn)       BLOCK+
     11                     64 -TRAILING TYPE SPACE l
     12 < You' 11 haue to i nuent your own "fortunes".        Edit     them
     13   into an auailable   block,   one per line.   Then edit       the
     14 block number into line       11 aboue, where indicated.)
     15


200 LIST

      0   ANSWERS, CHAP. 10, CONT'D)
      1   PROB. 3)
      2   ANIMALS    . " RAT    OX    TIGER RRBBITDRRGONSNRKEHORSE RAM           M
      3 ONKEYCOCK DOG      BORR
      4   .ANIMAL    ( u -- )
      5       6 * ['J    ANIMALS 3 + + 6 -TRAILING TYPE
      6   .ANIMAL takes   an argument  from 0 to 11.>
      7
      8     CJUNEESHEE)   < yr -- )
      9          1900 - 12 MOD
     10            "YOU WERE BORN IN THE YEAR OF THE"             .ANIMAL
     11                               46 EMIT ( dot)             CR l
     12
     13     JUNEESHEE    CR
     14        "IN  WHAT YEAR WERE YOU BORN?"
     15       S0@   4 EXPECT 0 >IN ! 1 WORD NUMBER CR CJUNEESHEE)


Copyright    FORTH, Inc.                                  Starting    FORTH
1-8         Answers                                                       Starting      FORTH




201 LIST

       0        ANSWERS, CHAP. 10,    CONT'D >                EMPTY
       l        PROB. 4)
       2
       3        NAME      64   *   202 BLOCK+              24 -TRAILING     TYPE
       4        HAIR      64   *   202 BLOCK+     24 +     20 -TRAILING     TYPE
       5        EYES      64   *   202 BLOCK+     44   +   20 -TRAILING     TYPE
       6
       7   LETTER     CR CR        DUP DUP
       8     " DEAR " NAME         CR
       9 CR " YOU'RE THE ONLY ONE fOR ME. LET ME RUN MY FINGERS "
      10 CR " THROUGH YOUR NICE " HAIR. " HAIR.  LET ME LOOK INTO"
      11 CR " YOUR DEEP " EYES . "  EYES. "
      12
      13:  LETTERS   4 0 DO I LETTER LOOP
      14
      15


202 LIST

       0 LATICIA                          BLACK                    BROWN
       l ALICE                            BLONDE                   BLUE
       2 STACEY                           BROWN                    HAZEL
       3 BARBRRA                          BROWN                    GREEN
       4
       s
       6
       7
       8
       9
      10
      11
      12
      13
      14
      15


203 LIST

       0      ANSWERS, CHAP. 10, CONT'D )                    EMPTY
       l    ( PROB. 5)
       2    VARIABLE nsTART         222 nSTART ! ( file  begins   at block       222)
       3      ELEMENT      ( i ndex  --  acsr >
       4          2•   1024 /MOD nSTART@         + BLOCK + UPDATE
       5      Test virtual     array:>
       6      INIT-ARRAY       500 0 DO I       I ELEMENT       LOOP;
       7      .ARRRY     0 DO CR        I . SPACE I ELEMENT?       LOOP
       8
       9      Now make the virtual     array  i nto a file:>
      10      AVAILABLE      ( -- adr)    nsTART@    BLOCK UPDATE
      11    0 AVAILABLE !
      12    C Redef i ne ELEMENT to sk i p over AUAILRBLE:>
      13      ELEMENT     C index - - adrl
      14        1+ 2*     1024 /MOD nSTART@        + BLOCK + UPDATE
      15


Copyright        FORTH, Inc.         3/06/81     11 : 42       Starting     fORTH
APPENDIX 1                                                                  Answers      1-9




204 LIST

      0      ANSWERS, CHAP. 10,     CONT'D)
      1      PROB. 5, CONT'D)
      2
      3      PUT     c value          AVAILABLE@ ELEMENT               1 AVAILABLE+!
      4
      5      SHOW     ( -- >   AVAILABLE@ 0 DO              CR
      6                 I ELEMENT?      LOOP
      7
      8      ENTER     ( value1   value2   --   l   SWAP PUT         PUT
      9
     10      TABLE  RVAILABLE@ ?DUP IF
     11       CR 0 DO   I 8 MOD 0=  IF              CR THEN
     12             I ELEMENT@   8 U.R              LOOP CR
     13             THEN;
     14
     15


205 LIST
      0 ( ANSWERS, CHAP. 11)                          EMPTY
      1 ( PROB. 1 J
      2   LOADED-BY CREATE                 DOES>    @LOAD;
      3
      4 ( PROB. 2)
      5   BASED.   CREATE              DOES>@       BASE@    SWAP BASE
      6     SWAP      BASE
      7
      8       PROB. 3)
      9       PLURAL   C adr -- l   CREATE
     10         DOES>@ SWAP ?DUP IF 0 DO DUP EXECUTE LOOP THEN DROP
     11     'CR PLURAL CRS
     12     5 CRS
     13       BEEP   7 EMIT 20000 0 DO LOOP  'BEEP   PLURAL BEEPS
     14     4 BEEPS
     15

206 LIST
      0      ANSWERS, CHAP. 11,     CONT'D)
      1
      2      PROB. 4)
      3      TURNE    [COMPILE] DO;   IMMEDIATE
      4      RETURNE [COMPILE] LOOP       IMMEDIATE
      5      TRY   10 0 TURNE I.    RETURHE;
      6
      7      PROB. 5)
      8      ASCII    32 WORD 1+ C@ [COMPILE] LITERAL                       IMMEDIATE
      9      STAR    ASCII*  EMIT
     10
     11   PROB. 6)
     12   LOOPS    >IN@  SWAP 0 DO DUP >IN                   INTERPRET       LOOP     DROP
     13 10 LOOPS    CR 30 SPACES STAR
     14
     15


Copyright     FORTH, Inc.                                        Starting   FORTH
                              APPENDIX 2
                     FURTHER FEATURES OF polyFORTH

polyFORTH is a total         software development    environment   designed
especially      for the      professional    programmer.     polyFORTH is
currently    available        for the most popular     minicomputers     and
microprocessors.
In this book we've covered all the polyFORTH commands that might
be used in a high-level,   single-task application.  We've left out
several categories    of words that are also included in polyFORTH.
These categories   are:

The Assembler
All versions  of FORTH, not just polyFORTH, include an assembler
vocabulary.   Using the assembler, it is possible to code directly
in the assembly language of a particular  processor.
The assembler is primarily    used to code time-critical     words in a
real - time application.  Often an entire application     can be coded
in high - level FORTH, then after the application     has been tested,
critical   low-level words can be redefined  in machine code.
polyFORTH's      assembler     vocabulary     includes   interrupt-handling
capability.

Printing   Utility
polyFORTH provides a multiprogrammed task that sends output to a
printer  instead  of your terminal.   Among the printing  utility
commands are several     which list disk blocks in the standard
format of three to a page.

Date and Time Support
The current date and, when supported             by a system clock,     time of
day are maintained by the system.




                                        2-1
2-2                                                            Starting   FORTH




The Multiprogrammer

As many tasks as are needed, either      terminal or control    tasks, can
be easily     added.    A single   command builds   a new task, given
certain   size parameters.     Another command activates     the task and
gives it a specified     behavior.


Disking   Utility

polyFORTH includes      commands for copying entire         disks or portions
thereof, for error     checking, and for formatting        when it is needed
by the system.


Target    Compiler

polyFORTH provides     the capability    to develop   an application  that
ultimately   will run on . a different  processor,  in some cases even a
different   variety  of processor.     The compiled   code can either    be
executed   directly  or be compressed     and burned into ROM.

FORTH, Inc., which licenses            and sells polyFORTH, was founded in
1973 by the inventor             of FORTH, Charles          H. Moore,    and his
associates.        FORTH, Inc.        also provides      full  documentation,
hot-line     support,     educational        services     in all parts     of the
country,    software    options,      and custom application       programming.
For further     information       write or call      FORTH, Inc., 2309 Pacific
Coast     Hwy., Hermosa       Beach,      CA, 90254, 213/372-8493,       TWX 910
344-6408.
                               APPENDIX3
                            FORTH-79STANDARD
The purpose of FORTH-79 Standard         is to allow transportability     of
standard     FORTH programs     in source form among standard          FORTH
systems.     A program  written    according   to the Standard      will run
equivalently    on any FORTH system that adheres to the Standard.
The current Standard was developed         by the FORTH Standards  Team.
(The Standards      Team is not affiliated     with FORTH, Inc., but the
compan:t does have three        voting     members on the team.)    This
Standard      is a descendant   of FORTH- 78 (proposed    by the FORTH
International      Standards  Team) and before that of FORTH-77 (the
work of an informal group of European and American FORTH users).
Efforts    at standardization    go back as far as 1973, at Kitt Peak
Observatory     in Arizona.
Having voted     to accept     the FORTH-79 Standard,        FORTH, Inc.
revised i ts product line to adopt most of the Standard's          features
and naming conventions.          Of course the Standard       attempts     to
cover only a minimal system.         Therefore    it doesn't address many
powerful words and features       included   in FORTH, Inc. 's poly FORTH,
which represents    the state-of-the-art       in FORTH implementations.
In this book we've included       many words which we feel are likely
to be .adopted by future Standards.
A small number of issues raised by the FORTH- 79 Standard          remain
controversial.         In a few cases,    the functions    of words as
described      in this book don't follow the FORTH-79 Standard,         but
rather the FORTH, Inc. product line.        Most of these discrepancies
have been marked with footnotes;       however, a few are more general
in nature and deserve special discussion.
The most noticeable      difference     is in the length of the name field
for each dict i onary          entry.      The Standard    specifies     that
dictionary     entries   include      up to 31 characters   of the name to
avoid "collisions."       FORTH, Inc. implementations       use a count and
three characters       not only to save memory, but also to support
dictionary    search routines that are s i gni f icantly     faster than any
31 character       implementation         seen to date.     FORTH, Inc. is
presently    researching      algorithms     which may offer users greater
flexibility      in naming,       without     unacceptable     sacrifice    in
performance.
The FORTH-79 Standard   includes   a few words which change their
behavior depending   on a variable   called STATE, which indicates
whether the user is in "compile     mode."  One is G::J.In FORTH,


                                     3-1
3-2                                                       Starting   FORTH




Inc. implementations,        G3
                              is a compiling      word, and therefore     it
may only   be used inside       a colon    definition.       In FORTH-79
languages,   it has two functions:      if the system is in execution
mode, it will type the string      which follows       it at the terminal
from which it was just entered.

A more significant      controversy   related    to STATE is the behavior
of the word [:] (tick). In FORTH, Inc. languages,        tick always reads
the next word in the input stream when tick is executed.                 The
Standard     tick however,     has two behaviors:    when the system is in
execution     mode, it behaves      in the normal way, but in compile
mode it behaves       like ~ (bracket-tick-bracket);            that is, it
compiles    the address      of the next word in the definition         as a
literal.   To define     a word which must "tick"     the next word in the
input stream when the word is executed,         you must use the phrase
      [COMPILE] I

if you ' re using   the   Standard   tick   •
There's   one other difference     worth mentioning      here. The FORTH-79
Standard    does not make the assumption         that the [QQ]loop index
and limit will be kept on the return         stack.    Presumably  a system
may have a third stack.        For this reason,     the Standard   includes
the word R@ to copy the top value from the return stack onto the
parameter    stack.  In all systems      that we know of, however,         R@
would be identical   to the FORTH [!].
For more information    or for copies  of the FORTH-79 Standard,
write to the FORTH Interest  Group (FIG), P.O. Box 1105, San Carlos,
CA 94070.
                           APPENDIX 4
                      SUMMARYOF FORTH WORDS




word                  page             word             page
ARITHMETIC
                                       CHARACTERINPUT
Single-length
                                       KEY                284
+                        53            EXPECT             284
                         53            WORD               284
*                        53            TEXT               284
I                        53            COUNT              285
/MOD                     53
MOD                      53            CHARACTEROUTPUT
*/                      123
*/MOD                   123            CR                  27
U*                      177            SPACE               27
U/MOD                   177            SPACES              27
l+                      123            EMIT                27
1-                      123             "                  27
2+                      123            PAGE               143
2-                      123            TYPE               283
2*                      123            >TYPE              285
2/                      123            - TRAILING         283
ABS                     123
NEGATE                  123
                                       COMPARISONS
Double-length
                                       Single-length
D+                      178
D-                      178            =                 103
DNEGATE                 178                              103
DABS                    178            <                 103
                                       U<                177
Mixed-length                           >                 103
                                       0=                103
M+                      179            0<                103
M/                      179            0>                103
M*                      179            MIN               123
M*/                     179            MAX               123
                                       Double-length
ASCII CHARACTERS
AND EQUIVALENTS                        D=                179
                                       DO=               179
See table       on p. 157              D<                179
                                       DU<               179


                              4-1
4-2                                        starting     FORTH




      word             page   word               page

                              EDITOR COMMANDS
      DMIN              179   All appear   on pp. 84,5
      DMAX              178

      String                  INTERPRETATION
      -TEXT             285                            84
                                                      246
                              INTERPRET               246
      COMPILATION
      ,                 209   LOGIC
      C,                21~
      ['1               247   NOT                     103
      DOES>             313   AND                     103
      IMMEDIATE         313   OR                      103
      COMPILE           313
      [COMPILE]         313
      LITERAL           313   MEMORY
      [                 313
      1                 313                           209
                              @                       209
                              +!                      209
      CONSTANTS               C!                      209
                              C@                      209
      0                 210   2!                      210
      1                 210   2@                      210
      o.                210   MOVE                    284
                              CMOVE                   284
                              <CMOV~                  285
      DEFINING WORDS          FILL                    209
                              ERASE                   210
                         27   BLANK                   285
      1                  27   DUMP                    210
      CONSTANT          209
      VARIABLE          209
      CREATE            209   NUMBERINPUT CONVERSION
      2VARIABLE         210
      2CONSTANT         210   >BINARYor
                              CONVERT                 284
                              NUMBER                  285
      DICTIONARYMANAGEMENT
                              NUMBEROUTPUT
      FORGET             84
      EMPTY              84                            27
      ALLOT             209   U.R                     143
      HERE              246   u.                      177
                              D.                      179
                              D.R                     179
Starting   FORTH                                   4-3




word               page   word            page
NUMBERFORMATTING
                          STACK MANIPULATION
<#                 177
i                  177    Sin9le-len9th
#S                 178
HOLD               178    SWAP              53
SIGN               178    DUP               53
#>                 178    OVER              53
                          ROT               53
                          DROP              53
OPERATINGSYSTEM           ?DUP             103
Commands                  Double-length
ABORT"             103    2SWAP               53
?STACK             103    2DUP                53
EXECUTE            246    2OVER               53
QUIT               246    2DROP               53
EXIT               246
HEX                177
OCTAL              177    STRUCTURE CONTROL
DECIMAL            177
HERE               246    IF               103
PAD                246    ELSE             103
'S                 247    THEN             103
FORTH              246    DO               143
EDITOR             246    LOOP             143
ASSEMBLER          246    +LOOP            143
DEFINITIONS        246    /LOOP            177
                          LEAVE            143
User Variabl e s          BEGIN            143
                          UNTIL            143
so                 247    WHILE            143
SCR                247    REPEAT           143
R#                 247
BASE               247
H                  247    VIRTUAL MEMOR
                                      Y
CONTEXT            247
CURRENT            247    LIST              84
>IN                247    LOAD              84
BLK                247    FLUSH             84
OFFSET             247    COPY              84
                          WIPE              84
                          UPDATE           283
RETURNSTACK               EMPTY-BUFFERS    283
                          BLOCK            283
>R                  123   BUFFER           283
R>                  123   EXIT             246
I                   123
I'                  123
J                   123
I
