program pruebaVerdet
    implicit none
    
    real*8 :: pos(2) = [0.d0, 2.d0], vel(2) = [2.d0, 4.d0], acel(2) = [0.d0, 0.d0], nuevaAcel(2) = [0.d0, -9.8d0], hn = 0.0002d0
    integer*8 :: i

    do i=1, 20000
        call calculoVerdet(pos, vel, acel, nuevaAcel, hn)
    end do
    
    write(*,*) pos

    contains
        subroutine calculoVerdet(posicion, velocidad, aceleracionActual, nuevaAceleracion,h)
            real*8 :: posicion(2), velocidad(2), aceleracionActual(2), nuevaAceleracion(2), h
            
            posicion = posicion + h*velocidad + (h**2 / 2) * aceleracionActual
            velocidad = velocidad + h*0.5*(aceleracionActual + nuevaAceleracion)
            aceleracionActual = nuevaAceleracion
        end subroutine calculoVerdet
end program pruebaVerdet