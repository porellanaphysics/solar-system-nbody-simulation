program condIniFacil
    implicit none

    real*8 :: excentricidad(8), r_per(8), r_apo(8), masa(8), x(9), y(9), vx(9), vy(9), masaFinal(9), px, py
    real*8 :: sumax, sumay
    
    integer*8 :: unit_in, unit_out, i
    
    unit_in = 10
    unit_out = 20
    
    open(unit=unit_in, file="datosPlanetas.dat", status="old", action="read")
    open(unit=unit_out, file="estadoInicial.dat", status="unknown", action="write")
    
    do i = 1, 8
        read(unit_in, *) r_apo(i), r_per(i), excentricidad(i), masa(i)
    end do
    
    x(1) = 0.d0
    y(1) = 0.d0
    vx(1) = 0.d0
    vy(1) = 0.d0
    masaFinal(1) = 1.d0
    
    do i = 2, 9
        x(i) = r_apo(i-1)
        y(i) = 0.d0
        vx(i) = 0.d0
        vy(i) = sqrt((1 - excentricidad(i-1)) / r_apo(i-1))
        masaFinal(i) = masa(i-1)
    end do
    
    px = 0.d0
    py = 0.d0
    
    do i = 2, 9
        px = px + masaFinal(i) * vx(i)
        py = py + masaFinal(i) * vy(i)
    end do
    
    vx(1) = -px / masaFinal(1)
    vy(1) = -py / masaFinal(1)
    
    
    
    do i = 1, 9
        write(unit_out, *) x(i), y(i), vx(i), vy(i), masaFinal(i)
    end do

    
    close(unit_in)
    close(unit_out)


end program condIniFacil