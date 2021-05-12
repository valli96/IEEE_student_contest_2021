
## PySpice

- is a API on top of SPICE
- the simulation are done in SPICE
- the output are converted in Numpy arrays
- Matplotlib can be used to plot the results

[PySpice Overview](https://pyspice.fabrice-salvaire.fr/releases/v1.4/)

[Netlist components](https://pyspice.fabrice-salvaire.fr/releases/v1.4/api/PySpice/Spice/Netlist.html)

[Spice doc](https://psim.powersimtech.com/hubfs/PDF%20Tutorials/Level-2%20and%20SPICE%20Model%20Simulation,%20Loss%20Calculation/SPICE-User-Manual.pdf)

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

    for win installation use command (Important: Update version accordingly) : 
    pyspice-post-installation --install-ngspice-dll --ngspice-version 34

### nice to know

- it is possible to generate a **netlist** in **Spice** or even **KiCad** and import this

## PySpice Basics

##### needed libraries

    import PySpice
    import PySpice.Logging.Logging as Logging # to enabel data acquisition
    from PySpice.Spice.Netlist import Circuit
    from PySpice.Unit import * # nessasary if Volt, Ohm, And Amere should be used (10@u_V)

To use PySpice on Linux the line below is needed

    PySpice.Spice.Simulation.CircuitSimulator.DEFAULT_SIMULATOR = 'ngspice-subprocess'  # to fix the error OSError: cannot load library 'libngspice.so'

To start the data logging

    logger = Logging.setup_logging()

Create the circuit with the name: "Voltage Divider"

    circuit = Circuit('Voltage Divider')
   
To add components to the circuit first nodes must be determined. Than the syntax looks like that. 
**circuit.R('Name_component','Node_1', 'Node_2', value)**

    circuit.V('input', 'in', circuit.gnd, 10@u_V)
    circuit.R('1', 'in', 'out', 9@u_kOhm)
    circuit.R('2', 'out', circuit.gnd, 6@u_kOhm)

The created netlist can be printed with is commend

    print("the circuit netlist: \n\n", circuit)

After the netlist is ready the simulator instance can be created. Many values like temperature can be initialized 

    simulator = circuit.simulator()

After that analysis can be run with the following command

    analysis = simulator.operating_point()

This will creat a vector `analysis.nodes` which contains the names and simulated voltages.

With this the name and voltage of every node can be extracted. For example of the node `out`

    print(str(analysis.nodes['out']))
    print(float(analysis.nodes['out'])) # if the variable is forced in to a float is will give the voltage
