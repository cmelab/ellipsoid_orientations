import hoomd

def create_rigid_simulation(orientations, positions, n_rigids, rel_const_pos, pps_ff, init_gsd):
    rigid_simulation = hoomd.Simulation(device=hoomd.device.auto_select(), seed=1)
    rigid_simulation.create_state_from_gsd(filename=init_gsd)
    const_particle_types = ['ca', 'ca', 'ca', 'ca', 'sh', 'ca', 'ca']
    

    rigid = hoomd.md.constrain.Rigid()
    rigid.body['rigid'] = {
        "constituent_types":const_particle_types,
        "positions": rel_const_pos,
        "orientations": [(1.0, 0.0, 0.0, 0.0)]* len(rel_const_pos),
        }
    integrator = hoomd.md.Integrator(dt=0.005, integrate_rotational_dof=True)
    rigid_simulation.operations.integrator = integrator
    integrator.rigid = rigid
    rigid_centers_and_free = hoomd.filter.Rigid(("center", "free"))
    nvt = hoomd.md.methods.ConstantVolume(
        filter=rigid_centers_and_free,
        thermostat=hoomd.md.methods.thermostats.Bussi(kT=1.0))
    integrator.methods.append(nvt)
    
    cell = hoomd.md.nlist.Cell(buffer=0, exclusions=['body'])
    
    lj = hoomd.md.pair.LJ(nlist=cell)
    
    # use aa pps simulation to define lj and special lj forces between constituent particles
    for k, v in dict(pps_ff[0].params).items():
        lj.params[k] = v
        lj.r_cut[k] = 4.8
    
    lj.params[('rigid', ['rigid', 'ca', 'sh'])]= dict(epsilon=0, sigma=0)
    lj.r_cut[('rigid', ['rigid', 'ca', 'sh'])] = 0

    integrator.forces.append(lj)
    rigid_simulation.state.thermalize_particle_momenta(filter=rigid_centers_and_free,
                                             kT=1.0)
    thermodynamic_quantities = hoomd.md.compute.ThermodynamicQuantities(filter=hoomd.filter.All())

    rigid_simulation.operations.computes.append(thermodynamic_quantities)
    with rigid_simulation._state.cpu_local_snapshot as data:
        rtag = data.particles.rtag
        rigid_tags = rtag[:n_rigids]
        data.particles.orientation[rigid_tags] = orientations
        
        data.particles.position[rigid_tags] = positions

    rigid_simulation.run(0)
    print('potential energy: ', rigid_simulation.operations.computes[0].potential_energy)
    with rigid_simulation._state.cpu_local_snapshot as snap:
        rtag = snap.particles.rtag[:n_rigids]
        print('force: ', snap.particles.net_force[rtag])
    return rigid_simulation
