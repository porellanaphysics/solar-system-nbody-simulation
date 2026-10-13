program vectores
    implicit none

    real*8, dimension(1:10) :: x ! Vector de 1 a 10 elementos
    integer :: i
    
    ! Declaracion dinámica
    !N se lee de archivo
    
    real*8, dimension(:), allocatable :: y ! Allocatable es "ya te lo diré"
    integer :: N
    N = 10
    allocate(y(1:N)) ! Reserva de memoria
    deallocate(y) ! Liberar memoria

end program vectores