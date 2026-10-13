program rssFinal
    implicit none
    type :: planeta
        real*8 :: masa
        real*8 :: posicion(2), velocidad(2), aceleracion(2), nuevaAceleracion(2) ! Estos son las variables de estado
    end type planeta

    type(planeta) :: planetas(9)
    real*8 :: h, r_cm(2), sumaMasas, x(9), y(9), t, periodo(9), posYtierra1(9), posYtierra2(9)
    integer*8 :: i, unit_in, unit_out, k, paso, l, boleano(9)
    
    unit_in = 10
    unit_out = 20
    
    do l=1, 9
        boleano(l) = 0
    end do
    
    open(unit=unit_in, file="estadoInicial.dat", status="old", action="read")
    open(unit=unit_out, file="resultado.dat", status="unknown", action="write") 
    
    do i = 1, 9
        read(unit_in,*) planetas(i)%posicion(1), planetas(i)%posicion(2), &
            planetas(i)%velocidad(1), planetas(i)%velocidad(2), &
            planetas(i)%masa
    end do
    paso = 0

    call calculoAceleracion

    h = 0.00008
    
    write(*,*)  365/(h*58.1d0)

    t = 0.d0
    periodo = 0.d0
    do paso=1, 240000
        t = paso*h
        periodo = periodo + h
        do l = 1, 9
            posYtierra1(l) = planetas(l)%posicion(2)
        end do
        !posYtierra1 = planetas(4)%posicion(2)
        call actualizarEstados
        do l = 1, 9
            posYtierra2(l) = planetas(l)%posicion(2)
        end do
        
        do l = 1, 9
            if(posYtierra1(l)*posYtierra2(l) < 0.d0) then
                if (boleano(l) == 0) then
                    write(*,*) "Planeta ", l, periodo(l)*2*58.1
                    boleano(l) = 1
                end if
                periodo(l) = 0.d0
            end if
        end do
        
        do k=1, 9
            x(k) = planetas(k)%posicion(1)
            y(k) = planetas(k)%posicion(2)
        end do
        write(unit_out,*) t, (x(k), y(k), k=1, 9)
    end do
    
    
    close(unit_in)
    close(unit_out)
    

    contains
        subroutine calculoVerdet(posicion, velocidad, aceleracionActual, nuevaAceleracion)
            real*8 :: posicion(2), velocidad(2), aceleracionActual(2), nuevaAceleracion(2)
            
            posicion = posicion + h*velocidad + (h**2 / 2) * aceleracionActual
            velocidad = velocidad + h*0.5*(aceleracionActual + nuevaAceleracion)
            aceleracionActual = nuevaAceleracion
        end subroutine calculoVerdet
        
        subroutine calcVerdetRSS
            integer*8 :: i
            real*8 :: posicion(2), velocidad(2), aceleracionActual(2), nuevaAceleracion(2)
            
            do i = 1, 9
                !posicion = planetas(i)%posicion
                !velocidad = planetas(i)%velocidad
                !aceleracionActual = planetas(i)%aceleracion
                !nuevaAceleracion = planetas(i)%nuevaAceleracion
                
                !posicion = posicion + h*velocidad + (h**2 / 2) * aceleracionActual
                !velocidad = velocidad + h*0.5*(aceleracionActual + nuevaAceleracion)
                !aceleracionActual = nuevaAceleracion
                

                posicion = planetas(i)%posicion + h*planetas(i)%velocidad + (h**2 / 2) * planetas(i)%aceleracion
                velocidad = planetas(i)%velocidad + h*0.5*(planetas(i)%aceleracion + planetas(i)%nuevaAceleracion)
                aceleracionActual = planetas(i)%nuevaAceleracion

                planetas(i)%posicion = posicion
                planetas(i)%velocidad = velocidad
                planetas(i)%aceleracion = aceleracionActual
            end do 
            
        end subroutine calcVerdetRSS

        subroutine calculoAceleracion
            integer*8 :: i, j
            real*8 :: suma(2), resta(2), valor(2)
            
            do i = 1, 9
                suma = [0.d0, 0.d0]
                do j = 1, 9
                    if (i /= j) then
                        resta = planetas(i)%posicion - planetas(j)%posicion
                        valor = ((planetas(j)%masa * (resta)) / (sqrt(sum((resta)**2)) + 1.d-10)**3 )
                        suma = suma - valor

                        !if (MOD(paso, 50) == 0 .AND. i == 4 .AND. j == 1) then
                        !    write(*,*) sqrt(sum(valor**2))
                        !end if
                    end if
                    
                end do

                if (paso == 0) then
                    planetas(i)%aceleracion = suma
                else if(paso /= 0) then
                    planetas(i)%nuevaAceleracion = suma
                end if

                !planetas(i)%nuevaAceleracion = suma
            end do
        end subroutine calculoAceleracion

        subroutine actualizarEstados
            integer*8 :: i, j
            
            call calculoAceleracion
            
            call calcVerdetRSS

            
        end subroutine actualizarEstados
end program rssFinal