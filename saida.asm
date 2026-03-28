.data
historico: .space 800
num_0: .double 3.14
num_1: .double 2.0
num_2: .double 10.0
num_3: .double 3.0
num_4: .double 4.0
num_5: .double 5.0
num_6: .double 10
num_7: .double 3
num_8: .double 8
num_9: .double 1.0

.text
.global main
main:
    ldr sp, =0x20000000
    mov r2, #0
    ldr r0, =num_0
    vldr.f64 d0, [r0]
    vpush {d0}
    ldr r0, =num_1
    vldr.f64 d0, [r0]
    vpush {d0}
    vpop {d0, d1}
    vadd.f64 d2, d1, d0
    vpush {d2}
    vpop {d0}
    ldr r0, =historico
    add r0, r0, r2
    vstr.f64 d0, [r0]
    add r2, r2, #8
    vpush {d0}
    ldr r0, =num_2
    vldr.f64 d0, [r0]
    vpush {d0}
    ldr r0, =num_3
    vldr.f64 d0, [r0]
    vpush {d0}
    vpop {d0, d1}
    vsub.f64 d2, d1, d0
    vpush {d2}
    vpop {d0}
    ldr r0, =historico
    add r0, r0, r2
    vstr.f64 d0, [r0]
    add r2, r2, #8
    vpush {d0}
    ldr r0, =num_4
    vldr.f64 d0, [r0]
    vpush {d0}
    ldr r0, =num_5
    vldr.f64 d0, [r0]
    vpush {d0}
    vpop {d0, d1}
    vmul.f64 d2, d1, d0
    vpush {d2}
    vpop {d0}
    ldr r0, =historico
    add r0, r0, r2
    vstr.f64 d0, [r0]
    add r2, r2, #8
    vpush {d0}
    ldr r0, =num_2
    vldr.f64 d0, [r0]
    vpush {d0}
    ldr r0, =num_4
    vldr.f64 d0, [r0]
    vpush {d0}
    vpop {d0, d1}
    vdiv.f64 d2, d1, d0
    vpush {d2}
    vpop {d0}
    ldr r0, =historico
    add r0, r0, r2
    vstr.f64 d0, [r0]
    add r2, r2, #8
    vpush {d0}
    ldr r0, =num_6
    vldr.f64 d0, [r0]
    vpush {d0}
    ldr r0, =num_7
    vldr.f64 d0, [r0]
    vpush {d0}
    vpop {d0, d1}
    vcvt.s32.f64 s0, d0
    vcvt.s32.f64 s1, d1
    vmov r0, s0
    vmov r1, s1
    mov r4, r1
    mov r5, r0
    mov r6, #0
div_loop_27:
    cmp r4, r5
    blt div_end_27
    sub r4, r4, r5
    add r6, r6, #1
    b div_loop_27
div_end_27:
    vmov s2, r6
    vcvt.f64.s32 d2, s2
    vpush {d2}
    vpop {d0}
    ldr r0, =historico
    add r0, r0, r2
    vstr.f64 d0, [r0]
    add r2, r2, #8
    vpush {d0}
    ldr r0, =num_6
    vldr.f64 d0, [r0]
    vpush {d0}
    ldr r0, =num_7
    vldr.f64 d0, [r0]
    vpush {d0}
    vpop {d0, d1}
    vcvt.s32.f64 s0, d0
    vcvt.s32.f64 s1, d1
    vmov r0, s0
    vmov r1, s1
    mov r4, r1
    mov r5, r0
mod_loop_33:
    cmp r4, r5
    blt mod_end_33
    sub r4, r4, r5
    b mod_loop_33
mod_end_33:
    vmov s2, r4
    vcvt.f64.s32 d2, s2
    vpush {d2}
    vpop {d0}
    ldr r0, =historico
    add r0, r0, r2
    vstr.f64 d0, [r0]
    add r2, r2, #8
    vpush {d0}
    ldr r0, =num_1
    vldr.f64 d0, [r0]
    vpush {d0}
    ldr r0, =num_8
    vldr.f64 d0, [r0]
    vpush {d0}
    vpop {d0, d1}
    vcvt.s32.f64 s0, d0
    vcvt.s32.f64 s1, d1
    vmov r0, s0
    vmov r1, s1
    mov r4, r0
    mov r5, r1
    mov r6, #1
pow_loop_39:
    cmp r4, #0
    beq pow_end_39
    mul r6, r6, r5
    sub r4, r4, #1
    b pow_loop_39
pow_end_39:
    vmov s2, r6
    vcvt.f64.s32 d2, s2
    vpush {d2}
    vpop {d0}
    ldr r0, =historico
    add r0, r0, r2
    vstr.f64 d0, [r0]
    add r2, r2, #8
    vpush {d0}
    ldr r0, =num_3
    vldr.f64 d0, [r0]
    vpush {d0}
    ldr r0, =num_1
    vldr.f64 d0, [r0]
    vpush {d0}
    vpop {d0, d1}
    vmul.f64 d2, d1, d0
    vpush {d2}
    ldr r0, =num_4
    vldr.f64 d0, [r0]
    vpush {d0}
    vpop {d0, d1}
    vadd.f64 d2, d1, d0
    vpush {d2}
    vpop {d0}
    ldr r0, =historico
    add r0, r0, r2
    vstr.f64 d0, [r0]
    add r2, r2, #8
    vpush {d0}
    ldr r0, =num_2
    vldr.f64 d0, [r0]
    vpush {d0}
    ldr r0, =num_1
    vldr.f64 d0, [r0]
    vpush {d0}
    vpop {d0, d1}
    vdiv.f64 d2, d1, d0
    vpush {d2}
    ldr r0, =num_3
    vldr.f64 d0, [r0]
    vpush {d0}
    ldr r0, =num_9
    vldr.f64 d0, [r0]
    vpush {d0}
    vpop {d0, d1}
    vsub.f64 d2, d1, d0
    vpush {d2}
    vpop {d0, d1}
    vmul.f64 d2, d1, d0
    vpush {d2}
    vpop {d0}
    ldr r0, =historico
    add r0, r0, r2
    vstr.f64 d0, [r0]
    add r2, r2, #8
    vpush {d0}
    ldr r0, =num_1
    vldr.f64 d0, [r0]
    vpush {d0}
    ldr r0, =num_7
    vldr.f64 d0, [r0]
    vpush {d0}
    vpop {d0, d1}
    vcvt.s32.f64 s0, d0
    vcvt.s32.f64 s1, d1
    vmov r0, s0
    vmov r1, s1
    mov r4, r0
    mov r5, r1
    mov r6, #1
pow_loop_70:
    cmp r4, #0
    beq pow_end_70
    mul r6, r6, r5
    sub r4, r4, #1
    b pow_loop_70
pow_end_70:
    vmov s2, r6
    vcvt.f64.s32 d2, s2
    vpush {d2}
    ldr r0, =num_4
    vldr.f64 d0, [r0]
    vpush {d0}
    ldr r0, =num_1
    vldr.f64 d0, [r0]
    vpush {d0}
    vpop {d0, d1}
    vdiv.f64 d2, d1, d0
    vpush {d2}
    vpop {d0, d1}
    vadd.f64 d2, d1, d0
    vpush {d2}
    vpop {d0}
    ldr r0, =historico
    add r0, r0, r2
    vstr.f64 d0, [r0]
    add r2, r2, #8
    vpush {d0}
    b .