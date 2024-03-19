import numpy as np

def get_frametime(reads1, skips1, reads2, ngroups, skips2 = 0, slow_size = 2040, fast_size = 256, noutput = 1, add_reset = True, interleaved_ref_pix = 1, nfastresets = 2048):

    if fast_size <= 8:

        f_oh = 3

    else:

        f_oh = 2

    # First, calculate reads1 frametime in seconds:
    if reads1 != 0:

        if add_reset:

            first_read_reset = ( ( fast_size / noutput ) + 12 ) * ( reads1 + interleaved_ref_pix + f_oh ) * 1 * 10 * 1e-6

        else:

            first_read_reset = 0.

        first_read = ( ( fast_size / noutput ) + 12 ) * ( reads1 + interleaved_ref_pix + f_oh ) * ngroups * 10 * 1e-6
        first_read_photon_collecting = ( fast_size / noutput ) * (reads1) * 10 * 1e-6 * ngroups

    else:

        first_read_photon_collecting = 0.
        first_read_reset = 0.
        first_read = 0.

    # Then, calculate the rest of the detector read via reads2 and skips2 for a single stripe:
    second_read = ( ( fast_size / noutput ) + 12 ) * ( reads2 + interleaved_ref_pix + f_oh ) * ngroups * 10 * 1e-6
    second_read_photon_collecting = ( fast_size / noutput ) * (reads2) * 10 * 1e-6 * ngroups

    if add_reset:

        second_read_reset = ( ( fast_size / noutput ) + 12 ) * ( reads2 + interleaved_ref_pix + f_oh ) * 1 * 10 * 1e-6

    else:

        second_read_reset = 0.

    # Get total by multiplying this per-stripe number for the total number of stripes to fill the slow_size:
    total_second_read = ( slow_size / reads2 ) * second_read
    total_second_read_reset = ( slow_size / reads2 ) * second_read_reset
    total_photon_collecting_second_read = ( slow_size / reads2 ) * second_read_photon_collecting

    # Fast row reset time in seconds per integration, per stripe:
    frrt = (slow_size / reads2) * 10 * 1e-6 * nfastresets

    # And calculate total of the entire detector:
    total = first_read + first_read_reset + total_second_read + total_second_read_reset + frrt

    # Save to dicts:
    out = {}
    out['frametime'] = total
    out['frametime photon-collecting'] = first_read_photon_collecting + total_photon_collecting_second_read
    out['frametime overheads'] = out['frametime'] - out['frametime photon-collecting']
    out['frametime per stripe2'] = second_read + second_read_reset
    out['frametime per stripe1'] = first_read + first_read_reset 

    return out
