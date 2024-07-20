# locators for x and y axes
minor_locator_x = AutoMinorLocator(8)
minor_locator_y = AutoMinorLocator(4)
# Plotting the laboratory frame's beam
fig, ax = plt.subplots(figsize=(8,6))
plt.hist(elab_sampled, bins=nbins_lab, range=(low_bound_lab,upper_bound_lab), label="Positron energy", density=True)
ax.axvline(x=E_lab, color='red', linestyle='dashed', label="Nominal energy\n$E^{lab}_0 = "+str(round(E_lab,2))+"\hspace{0.5}GeV$")
ax.axvline(x=E_lab_thr, color='black', linestyle='dotted', label="Energy threshold\n$E^{lab}_{thr} = "+str(round(E_lab_thr,2))+"\hspace{0.5}GeV$")
# setting properties
ax.set_xlim(low_bound_lab,upper_bound_lab)
ax.xaxis.set_minor_locator(minor_locator_x)
ax.yaxis.set_minor_locator(minor_locator_y)
ax.tick_params(axis='both', which='major', labelsize=15, length=10, direction='in', top=True, right=True)
ax.tick_params(axis='both', which='minor', labelsize=8, length=5, direction='in', top=True, right=True)
# setting labels and title
ax.set_xlabel("Energy (GeV)", fontsize=15,loc='right')
ax.set_ylabel(h_ylabel_lab, fontsize=15, loc='top')
ax.set_title(r"$\bf{Positron\hspace{0.5}energy}$: laboratory frame", fontsize=20, style='italic', loc='left')
ax.legend(loc=1, fontsize=12, frameon=False)

# Threshold region zoom-in
axins = ax.inset_axes([0.66,0.365,0.3,0.3])
axins.ticklabel_format(axis='y', style='scientific', useMathText=True, scilimits=(0,0.001))
axins.set_xlim(43, 44.25)
axins.set_ylim(0.,0.001)
axins.hist(elab_sampled, bins=nbins_lab, range=(low_bound_lab,upper_bound_lab), density=True)
axins.axvline(x=E_lab_thr, color='black', linestyle='dotted')
axins.yaxis.set_minor_locator(AutoMinorLocator(2))
axins.xaxis.set_minor_locator(AutoMinorLocator(2))
axins.tick_params(axis='both', which='major', labelsize=8, length=8, direction='in', top=True, right=True)
axins.tick_params(axis='both', which='minor', labelsize=4, length=4, direction='in', top=True, right=True)
ax.indicate_inset_zoom(axins)
