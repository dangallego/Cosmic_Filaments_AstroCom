# fil_plotter.py

#function created by Janvi Madhani for use in plotting filaments using dictionary she created
def plot_dm_filament(filament_idx,filament_dict,ax,colorfil='slateblue'):
    '''Helps plot filaments'''
    nsamp = filament_dict['filaments'][filament_idx]['nsamp'] 
    positions = filament_dict['filaments'][filament_idx]['px,py,pz']
    #plot the samples in between
    px = []
    py = []
    pz = []   
    for i in range(nsamp):
        px_,py_,pz_ = positions[i][0],positions[i][1],positions[i][2]
        px.append(px_)
        py.append(py_)
        pz.append(pz_)

    fil_line = ax.plot3D(px,py,pz,c=colorfil,lw = '2',alpha=0.4)
    

voids = fm.dict_slice(crit_points, 'cp_idx',0)
walls = fm.dict_slice(crit_points, 'cp_idx',1)
saddles = fm.dict_slice(crit_points, 'cp_idx',2)   #filament saddles
peaks = fm.dict_slice(crit_points, 'cp_idx',3)     #peaks -- nodes! 
bi_points = fm.dict_slice(crit_points, 'cp_idx',4) #bifurcation points

#Make scatter plot 
fig = plt.figure(figsize=[8,8]) ; ax = fig.add_subplot(projection='3d')
ax.set_box_aspect([1,1,1])

for fil_idx in range(nfils): #plots the filaments 
    fm.plot_dm_filament(fil_idx,filament_dm_dict,ax)
#        plots the critical points
x,y,z = fm.cp_plotter(voids) ; ax.scatter(x,y,z, label = 'Voids', c = 'k', s = 200, alpha = 0.1)
x,y,z = fm.cp_plotter(walls) ; ax.scatter(x,y,z, label = 'Walls', s = 25, alpha = 0.5, c = 'gold')
x,y,z = fm.cp_plotter(peaks) ; ax.scatter(x,y,z, label = 'Nodes', s = 100, alpha = 0.5, c = 'tomato')
x,y,z = fm.cp_plotter(bi_points) ; ax.scatter(x,y,z, label = 'Bi. Points', s = 10, alpha = 0.5, c = 'k')
###      saddles
#x,y,z = myfunctions.cp_plotter(saddles) ; ax.scatter(x,y,z, label = 'Saddles', s = 40, alpha = 0.4, c = 'darkturquoise')
#x,y,z = myfunctions.cp_plotter(real_saddles) ; ax.scatter(x,y,z, label = 'Saddles (no boundary)', s = 40, alpha = 0.4, c = 'darkturquoise')
x,y,z = fm.cp_plotter(saddles_nfils) ; ax.scatter(x,y,z, label = 'Saddles w/ nfils=2', s = 40, alpha = 0.4, c = 'darkturquoise')

ax.legend()
extent = 10
ax.set_xlim(-extent,extent)
ax.set_ylim(-extent,extent)
ax.set_zlim(-extent,extent)
plt.show()