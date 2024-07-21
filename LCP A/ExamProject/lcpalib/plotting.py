import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import matplotlib.ticker as ticker
from matplotlib import animation

def EnergyPlotPad(data, nbins, datarange, ax,
                  plotlabel="",
                  plotlabel_err="",
                  figtitle="",
                  xlabel="",
                  ylabel="",
                  title_size=15, 
                  xaxislabel_size=12,
                  yaxislabel_size=12,
                  alpha=0.7,
                  minloc_x=8,
                  minloc_y=4,
                  majorlabel_size=12,
                  minorlabel_size=8,
                  zoomin_limits=(0,0),
                  zoomin_xlims=(0,0),
                  zoomin_ylims=(0,0),
                  E_thr=0,
                  E_peak=0,
                  x_or_y_sci='x',
                  nomenergy_label="",
                  threnergy_label="",
                  title_loc='left'
                  ):
    # locators for x and y axes
    minor_locator_x = AutoMinorLocator(minloc_x)
    minor_locator_y = AutoMinorLocator(minloc_y)

    # computing counts and errors
    counts, edges = np.histogram(data, bins=nbins, range=datarange)
    errs = np.sqrt(counts)/((edges[1]-edges[0])*np.sum(counts))
    counts, edges, _ = ax.hist(data,bins=nbins,range=datarange,density=True,alpha=alpha,label=plotlabel)
    centers = 0.5*(edges[1:]+edges[:-1])
    ax.errorbar(centers, counts, yerr=errs, fmt='o', capsize=2, markersize=2.5, label=plotlabel_err)

    # vertical lines
    ax.axvline(x=E_peak, color='red', linestyle='dashed', label=nomenergy_label)
    ax.axvline(x=E_thr, color='black', linestyle='dotted', label=threnergy_label)

    # setting properties
    ax.set_xlim(datarange[0], datarange[1])
    ax.xaxis.set_minor_locator(minor_locator_x)
    ax.yaxis.set_minor_locator(minor_locator_y)
    ax.tick_params(axis='both', which='major', labelsize=majorlabel_size, length=10, direction='in', top=True, right=True)
    ax.tick_params(axis='both', which='minor', labelsize=minorlabel_size, length=5, direction='in', top=True, right=True)

    # setting labels and title
    ax.set_xlabel(xlabel, fontsize=xaxislabel_size,loc='right')
    ax.set_ylabel(ylabel, fontsize=yaxislabel_size,loc='top')
    ax.set_title(figtitle, fontsize=title_size, style='italic', loc=title_loc)

    # zoom-in region
    axins = ax.inset_axes([0.08,0.62,0.3,0.3])
    axins.ticklabel_format(axis=x_or_y_sci, style='scientific', useMathText=True, scilimits=zoomin_limits)
    axins.set_xlim(zoomin_xlims[0], zoomin_xlims[1])
    axins.set_ylim(zoomin_ylims[0], zoomin_ylims[1])
    axins.hist(data, bins=nbins, range=datarange, density=True, alpha=alpha)
    axins.axvline(x=E_thr, color='black', linestyle='dotted')
    axins.yaxis.set_minor_locator(AutoMinorLocator(2))
    axins.xaxis.set_minor_locator(AutoMinorLocator(4))
    axins.tick_params(axis='both', which='major', labelsize=8, length=8, direction='in', top=True, right=True)
    axins.tick_params(axis='both', which='minor', labelsize=4, length=4, direction='in', top=True, right=True)
    ax.indicate_inset_zoom(axins)

    # legend
    ax.legend(loc=1, fontsize=10, frameon=False)



def AnglePlotPad(angle_deg_dist, s_dist, cs_pdf, ax,
                 angledist_label="",
                 hist_type='bar',
                 hist_color=None,
                 alpha=0.7,
                 figtitle="",
                 title_size=15, 
                 xaxislabel_size=12,
                 yaxislabel_size=12,
                 minloc_x=10,
                 minloc_y=4,
                 nbins=60,
                 minth_label='Theoretical\n$\min(\sqrt{s})$',
                 minth_color='black',
                 maxth_label='Theoretical\n$\max(\sqrt{s})$',
                 maxth_color='black',
                 err_label='Count errs.\n(Poisson)',
                 err_color='red',
                 draw_minmaxth=True
                 ):
    #counts, edges, _ = ax.hist(angle_deg_dist, bins=60, range=(0,180), linewidth=1, density=True, label=angledist_label,alpha=alpha)
    counts, edges, _ = ax.hist(angle_deg_dist, bins=nbins, range=(0,180), linewidth=1, density=True, color=hist_color, label=angledist_label,alpha=alpha, histtype=hist_type)
    centers = 0.5*(edges[1:]+edges[:-1])
    bsize = edges[1]-edges[0]
    errs = np.sqrt(counts)/(bsize*len(counts))
    # now to add the 'theoretical' curve
    x_angles = np.linspace(0, 180, num=len(s_dist))
    minv = min(s_dist)
    maxv = max(s_dist)
    # plotting the theoretical curves
    if draw_minmaxth:
        ax.plot(x_angles, cs_pdf((2*minv)**2, x_angles*np.pi/180)*np.pi/180, color=minth_color, linestyle='dotted', label=minth_label)
        ax.plot(x_angles, cs_pdf((2*maxv)**2, x_angles*np.pi/180)*np.pi/180, color=maxth_color, linestyle='dashed', label=maxth_label)
    # plotting the count errors
    ax.errorbar(centers, counts, yerr=errs, capsize=2, fmt='o', markersize=2.5, color=err_color, linewidth=0.5, label=err_label)
    # setting options
    ax.set_xlabel("Angle (deg)", fontsize=xaxislabel_size,loc='right')
    ax.set_ylabel("Fraction of Counts / "+str(bsize)+" deg", fontsize=yaxislabel_size, loc='top')
    ax.ticklabel_format(axis='y', style='scientific', useMathText=True, scilimits=(0.,0.01))
    ax.tick_params(axis='both', which='major', labelsize=12, length=10, direction='in', top=True, right=True)
    ax.tick_params(axis='both', which='minor', labelsize=8, length=5, direction='in', top=True, right=True)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(30))
    minor_locator_x = AutoMinorLocator(minloc_x)
    minor_locator_y = AutoMinorLocator(minloc_y)
    ax.xaxis.set_minor_locator(minor_locator_x)
    ax.yaxis.set_minor_locator(minor_locator_y)
    ax.set_title(figtitle, fontsize=title_size, style='italic', loc='right')
    ax.legend(loc=2, fontsize=10, frameon=False)


def MuonPlotsCOMPads(ax, energies_df,
                 n_maj_loc=5,
                 n_min_loc=5,
                 plot_features=['CoM_Muon_px', 'CoM_Muon_py', 'CoM_Muon_pz'],
                 plot_labels=['x', 'y', 'z'],
                 xrange=(-0.03,0.03),
                 alpha=0.7,
                 title_size=15,
                 ylabel_size=12,
                 xlabel_size=12,
                 ticksize_major=12,
                 ticksize_minor=12,
                 legend_size=10,
                 histtype=None,
                 legend=False,
                 legend_frame=False,
                 legend_loc=0,
                 legend_bg=None,
                 legend_a=1,
                 plotlabel="",
                 errlabel="",
                 plot_color=None,
                 err_color=None
                 ):
    # intializing locators
    minor_locator_x = AutoMinorLocator(n_min_loc)
    minor_locator_y = AutoMinorLocator(4)
    major_locator_x = ticker.MaxNLocator(n_maj_loc)

    # initializing bins
    nbins=n_maj_loc*(n_min_loc-1)
    bin_size = (xrange[1]-xrange[0])/nbins

    # plot cycle for the various pads
    for p in range(0,len(plot_features),1):
        # setting labels
        xlabel = r'$p_{'+plot_labels[p]+'}$ (GeV)'
        ylabel = r"Fraction of Counts / ($"+str(round(bin_size,3)*10**3)+"\cdot10^{-3}$ GeV)"
        title = r'$\bf{\mu^{-}\hspace{0.5}p_{'+plot_labels[p]+'}}$ COM frame'

        # plotting
        counts, edges = np.histogram(energies_df[plot_features[p]], bins=nbins, range=xrange)
        errs = np.sqrt(counts)/((edges[1]-edges[0])*np.sum(counts))
        if histtype is not None:
            counts, edges, _ = ax[p].hist(energies_df[plot_features[p]],bins=nbins,range=xrange,density=True,histtype=histtype,alpha=alpha,label=plotlabel,color=plot_color)
        else:
            counts, edges, _ = ax[p].hist(energies_df[plot_features[p]],bins=nbins,range=xrange,density=True,alpha=alpha,label=plotlabel,color=plot_color)
        centers = 0.5*(edges[1:]+edges[:-1])
        ax[p].errorbar(centers, counts, yerr=errs, fmt='o', capsize=2, markersize=2.5,label=errlabel, color=err_color)

        # setting options
        ax[p].set_title(title,fontsize=title_size, loc='right')
        ax[p].set_ylabel(ylabel,fontsize=ylabel_size, loc='top')
        ax[p].set_xlabel(xlabel,fontsize=xlabel_size, loc='right')
        ax[p].xaxis.set_minor_locator(minor_locator_x)
        ax[p].yaxis.set_minor_locator(minor_locator_y)
        ax[p].xaxis.set_major_locator(major_locator_x)
        ax[p].ticklabel_format(axis='y', style='scientific', useMathText=True, scilimits=(0.,1))
        ax[p].tick_params(axis='both', which='major', labelsize=ticksize_major, length=10, direction='in', top=True, right=True)
        ax[p].tick_params(axis='both', which='minor', labelsize=ticksize_minor, length=5, direction='in', top=True, right=True)

        # legend
        if legend:
            ax[p].legend(loc=legend_loc, fontsize=legend_size, frameon=legend_frame, facecolor=legend_bg, framealpha=legend_a)



def MuonPlotsLABPads(ax, energies_df,
                 n_maj_loc=5,
                 n_min_loc=5,
                 plot_features=['LAB_Muon_px', 'LAB_Muon_py', 'LAB_Muon_pz'],
                 plot_labels=['x', 'y', 'z'],
                 xrange_xy=(-0.03,0.03),
                 xrange_z=(16,32),
                 nbins_z=32,
                 alpha=0.7,
                 title_size=15,
                 ylabel_size=12,
                 xlabel_size=12,
                 ticksize_major=15,
                 ticksize_minor=8,
                 legend_size=10,
                 histtype=None,
                 legend=False,
                 legend_loc=0,
                 legend_bg=None,
                 legend_frame=False,
                 legend_a=1,
                 plotlabel="",
                 errlabel="",
                 minloc_x_z=8,
                 maxloc_x_z=5,
                 plot_color=None,
                 err_color=None,

                 ):
    # initializing
    xrange = None
    nbins = n_maj_loc*(n_min_loc-1)
    bin_size = None
    
    # looping
    for p in range(0,len(plot_features),1):
        minor_locator_x = AutoMinorLocator(n_min_loc)
        minor_locator_y = AutoMinorLocator(4)
        major_locator_x = ticker.MaxNLocator(n_maj_loc)

        # setting labels
        xlabel = r'$p_{'+plot_labels[p]+'}$ (GeV)'
        ylabel = ''

        if p < 2:
            xrange = xrange_xy
            bin_size = (xrange[1]-xrange[0])/nbins
            ylabel = r"Fraction of Counts / ($"+str(round(bin_size,3)*10**3)+"\cdot10^{-3}$ GeV)"
        else:
            xrange = xrange_z
            nbins = nbins_z
            bin_size = (xrange[1]-xrange[0])/nbins        
            minor_locator_x = AutoMinorLocator(minloc_x_z)
            major_locator_x = ticker.MaxNLocator(maxloc_x_z)
            ylabel = r"Fraction of Counts / ($"+str(round(bin_size,3))+"$ GeV)"
        
        title = r'$\bf{\mu^{-}\hspace{0.5}p_{'+plot_labels[p]+'}}$ LAB frame'

        # plotting
        counts, edges = np.histogram(energies_df[plot_features[p]], bins=nbins, range=xrange)
        errs = np.sqrt(counts)/((edges[1]-edges[0])*np.sum(counts))
        # making the histogram
        if histtype is not None:
            counts, edges, _ = ax[p].hist(energies_df[plot_features[p]],bins=nbins,range=xrange,density=True,alpha=alpha,histtype=histtype,label=plotlabel,color=plot_color)
        else:
            counts, edges, _ = ax[p].hist(energies_df[plot_features[p]],bins=nbins,range=xrange,density=True,alpha=alpha,label=plotlabel,color=plot_color)
        centers = 0.5*(edges[1:]+edges[:-1])
        ax[p].errorbar(centers, counts, yerr=errs, fmt='o', capsize=2, markersize=2.5, label=errlabel, color=err_color)

        # setting options
        ax[p].set_title(title,fontsize=title_size, loc='right')
        ax[p].set_ylabel(ylabel,fontsize=ylabel_size, loc='top')
        ax[p].set_xlabel(xlabel,fontsize=xlabel_size, loc='right')
        ax[p].xaxis.set_minor_locator(minor_locator_x)
        ax[p].yaxis.set_minor_locator(minor_locator_y)
        ax[p].xaxis.set_major_locator(major_locator_x)
        ax[p].ticklabel_format(axis='y', style='scientific', useMathText=True, scilimits=(0.,1))
        ax[p].tick_params(axis='both', which='major', labelsize=ticksize_major, length=10, direction='in', top=True, right=True)
        ax[p].tick_params(axis='both', which='minor', labelsize=ticksize_minor, length=5, direction='in', top=True, right=True)

        # legend
        if legend:
            ax[p].legend(loc=legend_loc, fontsize=legend_size, frameon=legend_frame, facecolor=legend_bg, framealpha=legend_a)


def MuonTracks(ax, energies_df, scaled_energies,
               beam_axis=[-20,20],
               n_tracks = 50,
               figtitle = "",
               beam_energy = 0,
               frame = "CoM",
               axes3d_xlim = [0,0],
               axes3d_ylim = [0,0],
               axes3d_zlim = [0,0],
               text_xyz_lab1 = [0,0,0],
               text_xyz_lab2 = [0,0,0]
               ):
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    # Now set color to white (or whatever is "invisible")
    ax.xaxis.pane.set_edgecolor('black')
    ax.yaxis.pane.set_edgecolor('black')
    ax.zaxis.pane.set_edgecolor('black')

    # Getting rid of the grid
    ax.grid(False)
    ax.set_facecolor('black')

    # Plotting the beam axis
    ax.plot3D([beam_axis[0],beam_axis[1]],[0,0],[0,0],c='gold',linestyle='dashed')

    # Plotting the tracks
    xline = [0]
    yline = [0]
    zline = [0]

    for i in range(0,n_tracks,1):    
        ax.plot3D([0,energies_df[frame+'_Muon_pz'][i]],
                [0,energies_df[frame+'_Muon_px'][i]],
                [0,energies_df[frame+'_Muon_py'][i]],
                marker='',
                alpha=scaled_energies[i],
                color='r')
        ax.plot3D([0,energies_df[frame+'_AntiMuon_pz'][i]],
                [0,energies_df[frame+'_AntiMuon_px'][i]],
                [0,energies_df[frame+'_AntiMuon_py'][i]],
                marker='',
                alpha=scaled_energies[i],
                color='b')

        ax.axes.set_xlim3d(left=axes3d_xlim[0], right=axes3d_xlim[1])
        ax.axes.set_ylim3d(bottom=axes3d_ylim[0], top=axes3d_ylim[1]) 
        ax.axes.set_zlim3d(bottom=axes3d_zlim[0], top=axes3d_zlim[1])

        ax.set_title(figtitle,fontsize=20,color='white',loc='right')

        ax.text(text_xyz_lab1[0], text_xyz_lab1[1], text_xyz_lab1[2], s='Beam axis (z)', color='white', fontsize=20)
        ax.text(text_xyz_lab2[0], text_xyz_lab2[1], text_xyz_lab2[2], s='Beam energy: '+str(round(beam_energy,3))+' GeV', color='white', fontsize=20)


def EnergiesBeforeAfter(ax, energies, energies_reduced, energies_range, nbins,
                        label_0="",
                        label_1="",
                        E_lab_thr=0,
                        E_lab=0,
                        yaxis_label="",
                        alpha=0.7,
                        z_depth=3.0,
                        figtitle="Positron beam energy - LAB frame"
                        ):
    
    # plotting the distribution in z=0 cm
    counts, edges = np.histogram(energies, bins=nbins, range=energies_range)
    errs_l0 = np.sqrt(counts)/((edges[1]-edges[0])*np.sum(counts))
    # making the histogram
    counts_l0, edges_l0, _ = ax.hist(energies,bins=nbins,range=energies_range,density=True,alpha=alpha,label=label_0)
    centers_l0 = 0.5*(edges_l0[1:]+edges_l0[:-1])
    
    # plotting the distribution in z=3 cm
    counts, edges = np.histogram(energies_reduced, bins=nbins, range=energies_range)
    errs_l1 = np.sqrt(counts)/((edges[1]-edges[0])*np.sum(counts))
    # making the histogram
    counts_l1, edges_l1, _ = ax.hist(energies_reduced,bins=nbins,range=energies_range,density=True,alpha=alpha,label=label_1)
    centers_l1 = 0.5*(edges_l1[1:]+edges_l1[:-1])
    
    # plotting the error bars
    ax.errorbar(centers_l0, counts_l0, yerr=errs_l0, fmt='o', capsize=2, markersize=2.5)
    ax.errorbar(centers_l1, counts_l1, yerr=errs_l1, fmt='o', capsize=2, markersize=2.5)

    ax.axvline(x=E_lab_thr, color='black', linestyle='solid', label="$E_{thr} = "+str(round(E_lab_thr,2))+"$ GeV")
    ax.axvline(x=E_lab*np.exp(-z_depth/35.28), color='blue', linestyle='dashed', label="$E(z) = "+str(round(E_lab*np.exp(-z_depth/35.28),2))+"$ GeV")
    ax.axvline(x=E_lab, color='red', linestyle='dashed', label="$E(0) = "+str(round(E_lab,2))+"$ GeV")
    ax.set_xlim(energies_range[0],energies_range[1])
    ax.set_ylim(0,0.95)

    major_locator_x = ticker.MaxNLocator(8)
    minor_locator_x = AutoMinorLocator(8)
    minor_locator_y = AutoMinorLocator(4)
    ax.xaxis.set_major_locator(major_locator_x)
    ax.xaxis.set_minor_locator(minor_locator_x)
    ax.yaxis.set_minor_locator(minor_locator_y)

    ax.ticklabel_format(axis='y', style='scientific', useMathText=True, scilimits=(0.,0.01))
    ax.tick_params(axis='both', which='major', labelsize=12, length=10, direction='in', top=True, right=True)
    ax.tick_params(axis='both', which='minor', labelsize=8, length=5, direction='in', top=True, right=True)
    ax.set_title(figtitle,fontsize=15, loc='right')
    ax.set_ylabel(yaxis_label,fontsize=12, loc='top')
    ax.set_xlabel("Beam energy (GeV)",fontsize=12, loc='right')

    ax.legend(loc=0, fontsize=10, frameon=False)


def EnergiesBeforeAfterAnimation(filename, data, E_lab_thr, E_lab):
    fig, ax = plt.subplots(figsize=(8,6))
    depths = np.linspace(0,3,200)
    def update(depth_idx):
        ax.clear()
        EnergiesBeforeAfter(ax,
                            data,
                            data*np.exp(-depths[depth_idx]/35.28),
                            energies_range=(40,48),
                            nbins=64,
                            label_0="$z=0$ cm",
                            label_1="$z=3$ cm",
                            E_lab_thr=E_lab_thr,
                            E_lab=E_lab,
                            yaxis_label="Fraction of Counts / (0.125 GeV)",
                            alpha=0.7,
                            z_depth=depths[depth_idx]
                            )
    
    ani = animation.FuncAnimation(fig, update, frames=range(0,len(depths)))
    FFW = animation.FFMpegWriter(fps=20)
    ani.save(filename, writer=FFW) #imagemagick


def PositronInteractionEnergies(ax, data, nbins, datarange, xrange, yrange,
                                xminloc=4,
                                yminloc=5,
                                xlabel="",
                                ylabel="",
                                figtitle="", 
                                alpha=0.7,
                                legend=True,
                                histlabel="Events\nDistribution",
                                histerrlabel="Count Errors\n(Poisson)",
                                histerrcolor='black',
                                hist_type='bar',
                                hist_color=None
                                ):
    # setting options
    ax.set_xlim(xrange[0],xrange[1])
    ax.set_ylim(yrange[0],yrange[1])
    major_locator_x = ticker.MaxNLocator(8)
    minor_locator_x = AutoMinorLocator(xminloc)
    minor_locator_y = AutoMinorLocator(yminloc)
    ax.xaxis.set_major_locator(major_locator_x)
    ax.xaxis.set_minor_locator(minor_locator_x)
    ax.yaxis.set_minor_locator(minor_locator_y)
    ax.ticklabel_format(axis='y', style='scientific', useMathText=True, scilimits=(0.,0.01))
    ax.tick_params(axis='both', which='major', labelsize=12, length=10, direction='in', top=True, right=True)
    ax.tick_params(axis='both', which='minor', labelsize=8, length=5, direction='in', top=True, right=True)
    ax.set_title(figtitle, fontsize=15, loc='right')
    ax.set_ylabel(ylabel, fontsize=12, loc='top')
    ax.set_xlabel(xlabel, fontsize=12, loc='right')

    # plotting
    counts, edges = np.histogram(data, bins=nbins, range=datarange)
    errs = np.sqrt(counts)/((edges[1]-edges[0])*np.sum(counts))
    # plotting the counts
    counts, edges, _ = ax.hist(data,bins=nbins,range=datarange,density=True,alpha=alpha,label=histlabel,histtype=hist_type,color=hist_color)
    centers = 0.5*(edges[1:]+edges[:-1])

    # plotting the errorbars
    ax.errorbar(centers, counts, yerr=errs, fmt='o', capsize=2, markersize=2.5, c=histerrcolor,label=histerrlabel)

    # legend
    ax.legend(loc=2, fontsize=12, frameon=False)

