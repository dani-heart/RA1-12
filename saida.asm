.data
num_0: .double 2.0
num_1: .double 3
num_2: .double 4.0

.text
.global main
main:
    push {lr}
    ldr r0, =num_0
    vldr.f64 d0, [r0]
    vpush {d0}
    ldr r0, =num_1
    vldr.f64 d0, [r0]
    vpush {d0}
    vpop {d0, d1}
    vcvt.s32.f64 s0, d0
    vcvt.s32.f64 s1, d1
    vmov r0, s0
    vmov r1, s1
    bl pow
    mov r2, r0
    vmov s2, r2
    vcvt.f64.s32 d2, s2
    vpush {d2}
    ldr r0, =num_2
    vldr.f64 d0, [r0]
    vpush {d0}
    ldr r0, =num_0
    vldr.f64 d0, [r0]
    vpush {d0}
    vpop {d0, d1}
    vdiv.f64 d2, d1, d0
    vpush {d2}
    vpop {d0, d1}
    vadd.f64 d2, d1, d0
    vpush {d2}
    pop {pc}