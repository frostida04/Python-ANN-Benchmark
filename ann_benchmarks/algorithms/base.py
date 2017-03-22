from __future__ import absolute_import

class BaseANN(object):
    def use_threads(self):
        return True
    def done(self):
        pass
    def get_index_size(self, process):
	"""Returns the size of the index in kB or -1 if not implemented."""
	statusfile = open("/proc/%(pid)s/status" % {"pid" : str(process)}, "r")
	for line in statusfile.readlines():
	    if "VmRSS" in line:
		mem_usage = line.split(":")[1].strip()
		usage, unit = mem_usage.split(" ")
		val = int(usage)
		# Assume output to be in kB
		if val == "B":
			val /= 1000.0
		if val == "mB":
			val *= 1e3
		if val == "gB":
			val *= 1e6
		return val
	return -1
