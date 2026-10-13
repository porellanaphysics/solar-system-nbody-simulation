program condIni
    implicit none

    real*8 :: excentricidad(8), r_per(8), r_apo(8), r(8), theta(8), masa(8), p(8), a(8), coseno(8), sino(8)
    real*8 :: vt(8), vr(8), vx(8), vy(8), x(8), y(8), rIn(2), rPos(2), vIn(2), vPos(2), rCambio(2, 2)
    real*8 :: xi(8), yi(8), vxi(8), vyi(8)
    real*8, parameter :: UA = 1.495978707d8, Ms = 1.9885d30, PI = 3.141592653589793d0, g = 6.67430d-11
    real*8, parameter :: MU_SOL = g * Ms / (UA**3)
    integer*8 :: positivo(8), unit_in, unit_out, i
    character(len=50) :: nombre(8)
    
    unit_in = 10
    unit_out = 20
    
    open(unit=unit_in, file="datosReales.dat", status="old", action="read")
    open(unit=unit_out, file="estadoInicial.dat", status="replace", action="write")
    

    do i = 1, 8
        read(unit_in,*) nombre(i), excentricidad(i), r_per(i), r_apo(i), r(i), positivo(i), theta(i), masa(i)
    end do

    ! A partir de aquí lo que hago es reescalar las variables
    do i=1, 8
        masa(i) = masa(i)/Ms
        r_per(i) = r_per(i)/UA
        r_apo(i) = r_apo(i)/UA
        r(i) = r(i)/UA
        theta(i) = theta(i)*PI/180 ! Este sirve para cambiar de grados a radianes el angulo
    end do
    
    ! Por aquí empiezo el calculo de los vx, vy, xi, yi
    
    do i = 1, 8
        a(i) = 0.5 * (r_per(i) + r_apo(i))
        p(i) = a(i)*(1 - excentricidad(i)**2)
        coseno(i) = (p(i) / r(i) - 1) / excentricidad(i)
        if (positivo(i) == 1) then
            sino(i) = sqrt(1 - coseno(i)**2)
        else 
            sino(i) = -sqrt(1 - coseno(i)**2)
        end if
        
        vt(i) = sqrt(MU_SOL / p(i)) * (1 - excentricidad(i)*coseno(i))
        vr(i) = sqrt(MU_SOL / p(i)) * excentricidad(i) * sino(i)
        vx(i) = vr(i) * coseno(i) - vt(i) * sino(i)
        vy(i) = vr(i)* sino(i) + vt(i) * coseno(i)
        
        x(i) = r(i) * coseno(i)
        y(i) = r(i) * sino(i)
    end do
    
    ! Este codigo me cambia las coordenadas a las nuevas coordenadas
    do i = 1, 8
        rCambio = reshape((/ cos(theta(i)), -sin(theta(i)), sin(theta(i)), cos(theta(i)) /), shape=[2, 2])
        
        rIn = reshape((/ x(i), y(i) /), shape=[2])
        vIn = reshape((/ vx(i), vy(i) /), shape=[2])
        
        rPos = matmul(rCambio, rIn)
        vPos = matmul(rCambio, vIn)
        
        xi(i) = rPos(1)
        yi(i) = rPos(2)
        vxi(i) = vPos(1)
        vyi(i) = vPos(2)
        
        write(unit_out,*) xi(i), yi(i), vxi(i), vyi(i), masa(i)
        

    end do
    


    close(unit_in)
    close(unit_out)

end program condIni