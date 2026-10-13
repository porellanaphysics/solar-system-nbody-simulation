# Makefile for Solar System N-Body Simulation (RSS)
FC ?= gfortran
FFLAGS = -O3 -Wall -fdefault-real-8
PYTHON ?= python3

.PHONY: all clean run plot animate test

all: rssFinal condIni

rssFinal: src/rssFinal.f95
	$(FC) $(FFLAGS) -o $@ src/rssFinal.f95

condIni: src/condIni.f95
	$(FC) $(FFLAGS) -o $@ src/condIni.f95

run: rssFinal
	./rssFinal

plot:
	$(PYTHON) scripts/mostrarRes.py

animate:
	manim -pql scripts/manimPlan.py SistemaSolar

clean:
	rm -f rssFinal condIni condIniFacil pruebaVerdet pruebaAceleracion *.o *.mod resultado.dat

