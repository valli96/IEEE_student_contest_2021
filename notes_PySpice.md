
## PySpice

- is a API on top of SPICE
- the simulation are done in SPICE
- the output are converted in Numpy arrays
- Matplotlib can be used to plot the results

[PySpice Overview](https://pyspice.fabrice-salvaire.fr/releases/v1.4/)

[A greart short introduction to PySpice](https://www.slideshare.net/PoleSystematicParisRegion/pyparis2017-circuit-simulation-using-python-by-fabrice-salvaire)

[A example of a transmission line simulation](https://pyspice.fabrice-salvaire.fr/releases/v1.4/examples/transmission-lines/time-delay.html)


### installation of PySpice

    sudo apt install libngspice0
    pip install PySpice

For extra examples:

    pyspice-post-installation --download-example

### installation of Ngspice/Xyce

<!-- >??? -->  
<!-- > not yet found out -->
    sudo apt install Ngspice

### nice to know

- it is possible to generate a **netlist** in **Spice** or even **KiCad** and import this

