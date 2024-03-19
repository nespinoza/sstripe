import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('ticks')

import utils

"""
The code below only works for SOSS. Can create different ones for other instruments, but might require some mods.
"""

ncols = 2040
nrows = 256
ngroups = 2
bright_limit = 8.4 # In J-magnitude

stripe_sizes = np.arange(ncols)+1
print(stripe_sizes)
efficiency = np.zeros(len(stripe_sizes))

for i in range(len(stripe_sizes)):

    # Add reset is set to false because _it seems_ Eddie's equations already account for this:
    out = utils.get_frametime(reads1=0, skips1=0, 
                              reads2=stripe_sizes[i], skips2 = 0, 
                              ngroups=ngroups, 
                              fast_size = nrows, slow_size = ncols, add_reset = False, interleaved_ref_pix = 0)

    efficiency[i] = out['frametime photon-collecting'] / out['frametime']

plt.figure(figsize = (7,5))
plt.plot(stripe_sizes, efficiency*100, 'r-', lw = 3)
plt.xlabel('Size of stripe (reads2)', fontsize = 15)
plt.ylabel('Observation Efficiency (%)', fontsize = 15)
plt.xscale('log')
#plt.yscale('log')

plt.xlim(0.9,ncols + 1)
plt.ylim(0., 100)
plt.xticks([1, 10, 100, 1000], ['1', '10', '100', '1000'], fontsize = 14)
plt.yticks(fontsize = 14)
plt.tight_layout()
plt.savefig('efficiency.png')

# Now plot brightness limits as a function of stripe size; this assumes:
# - Bright limit for 256 subarray is magnitude 8.4 in Order 1.
# - If stripe is the same size as the full subarray (2040), the bright limit will be the same
# - If stripe is half the size, the bright limit will be (1/2) brighter in flux, or -2.51*log10(0.5) = 0.755 magnitudes brighter.
# - In general, if stripe is (stripesize / 2040), the bright limit would be -2.51*log10( stripesize / 2040 ) magnitudes brighter.

plt.figure(figsize = (7,5))
plt.plot(stripe_sizes, bright_limit + 2.51*np.log10( stripe_sizes / ncols ), 'r-', lw = 3)
plt.xlabel('Size of stripe (reads2)', fontsize = 15)
plt.ylabel('Bright limit (J-magnitude)', fontsize = 15)
plt.xscale('log')
#plt.yscale('log')

plt.xlim(0.9, ncols + 1)
#plt.ylim(0., 100)
plt.xticks([1, 10, 100, 1000], ['1', '10', '100', '1000'], fontsize = 14)
plt.yticks(fontsize = 14)
plt.tight_layout()
plt.savefig('bright_limit.png')
