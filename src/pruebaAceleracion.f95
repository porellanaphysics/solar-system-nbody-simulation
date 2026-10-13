program pruebaAceleracion
    implicit none

    type :: planeta
        real*8 :: masa
        real*8 :: posicion(2), velocidad(2), aceleracion(2) ! Estos son las variables de estado
    end type planeta

    type(planeta) :: planetas(8)
    integer*8 :: i=1
    
    planetas(1)%posicion = [1.d0, 0.d0]
    
    write(*,*) planetas(1)%posicion
    write(*,*) calculoNuevaAceleracion(i)
    
    contains
        function calculoRestaVectores(vectorInicial, vectorFinal) result(vectorResta)
            real*8 :: vectorInicial(2), vectorFinal(2), vectorResta(2)
            vectorResta = vectorInicial - vectorFinal
        end function calculoRestaVectores


        function calculoNuevaAceleracion(posicionVectorPlaneta) result(nuevaAceleracion)
            real*8 :: nuevaAceleracion(2), suma(2), restaVector(2)
            integer*8 :: posicionVectorPlaneta, i
            
            write(*,*) planetas(posicionVectorPlaneta)%posicion
            suma = - (planetas(posicionVectorPlaneta)%posicion)/(sqrt(sum(planetas(posicionVectorPlaneta)%posicion**2))**3)
            write(*,*) suma
            
            do i = 1, size(planetas)
                if (i /= posicionVectorPlaneta) then
                    restaVector = calculoRestaVectores(planetas(posicionVectorPlaneta)%posicion, planetas(i)%posicion)
                    suma = suma - (planetas(i)%masa * restaVector) / (sqrt(sum(restaVector**2))**3)
                end if
            end do
            
            !write(*,*) suma
            nuevaAceleracion = suma

        end function calculoNuevaAceleracion

    
end program pruebaAceleracion