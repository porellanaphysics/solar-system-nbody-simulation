program rss
    implicit none
    
    type :: planeta
        real*8 :: masa
        real*8 :: posicion(2), velocidad(2), aceleracion(2) ! Estos son las variables de estado
    end type planeta
    
    type(planeta) :: planetas(8)
    real*8 :: h = 0.03119d0
    real*8 :: x(8), y(8), t
    integer*8 :: unit_in, unit_out, paso, plan, k
    
    unit_in = 10
    unit_out = 20
    
    open(unit=unit_in, file="estadoInicial.dat", status="old", action="read")
    open(unit=unit_out, file="resultado.dat", status="replace", action="write")
    

    do k=1, 8
        read(unit_in,*) planetas(k)%posicion(1), planetas(k)%posicion(2), &
            planetas(k)%velocidad(1), planetas(k)%velocidad(2), &
            planetas(k)%masa
    end do
    
    write(*,*) planetas

    
    
    do paso=1, 650
        t = paso*h
        do plan=1, size(planetas)
            call calcNuevosParametros(plan)
            x(plan) = planetas(plan)%posicion(1)
            y(plan) = planetas(plan)%posicion(2)
        end do
        write(unit_out,*) t, (x(k), y(k), k=1, 8)
    end do
    

    close(unit_in)
    close(unit_out)
    

    contains
        ! Esta subrutina nos dará la nueva posición y la nueva velocidad a partir de la nueva aceleración ya calculada
        subroutine calculoVerdet(posicion, velocidad, aceleracionActual, nuevaAceleracion)
            real*8 :: posicion(2), velocidad(2), aceleracionActual(2), nuevaAceleracion(2)
            
            posicion = posicion + h*velocidad + (h**2 / 2) * aceleracionActual
            velocidad = velocidad + h*0.5*(aceleracionActual + nuevaAceleracion)
            aceleracionActual = nuevaAceleracion
        end subroutine calculoVerdet
        
        ! Esta función te calcula la resta entre dos vectores
        function calculoRestaVectores(vectorInicial, vectorFinal) result(vectorResta)
            real*8 :: vectorInicial(2), vectorFinal(2), vectorResta(2)
            vectorResta = vectorInicial - vectorFinal
        end function calculoRestaVectores

        ! Este algoritmo nos calculará la aceleración de cada planeta en función de la fuerza gravitatoria de los demás planetas
        function calculoNuevaAceleracion(posicionVectorPlaneta) result(nuevaAceleracion)
            real*8 :: nuevaAceleracion(2), suma(2), restaVector(2)
            integer*8 :: posicionVectorPlaneta, i
            suma = - (planetas(posicionVectorPlaneta)%posicion)/(sqrt(sum(planetas(posicionVectorPlaneta)%posicion**2))**3)
            
            do i = 1, size(planetas)
                if (i /= posicionVectorPlaneta) then
                    restaVector = calculoRestaVectores(planetas(posicionVectorPlaneta)%posicion, planetas(i)%posicion)
                    suma = suma - (planetas(i)%masa * restaVector) / (sqrt(sum(restaVector**2))**3)
                end if
            end do
            
            write(*,*) suma
            nuevaAceleracion = suma

        end function calculoNuevaAceleracion
        
        ! Esta subrutina cambiará los parametros del planeta a un nuevo planeta
        subroutine calcNuevosParametros(i) ! i es el índice del vector planetas | por la cara no puedo añadir frases muy largas
            integer*8 :: i
            real*8 :: nuevaAceleracion(2)

            nuevaAceleracion = calculoNuevaAceleracion(i)

            call calculoVerdet(planetas(i)%posicion, planetas(i)%velocidad, planetas(i)%aceleracion, nuevaAceleracion)


        end subroutine calcNuevosParametros
end program rss