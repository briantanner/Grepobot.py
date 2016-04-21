class Command:
	def __init__(self):
		pass

	def __str__(self):
		return self.__name__

	def __repr__(self):
		return self.__class__.__name__

	@property
	def aliases(self):
	    return self._aliases

	@property
	def doc(self):
	    return self._doc

	@property
	def usage(self):
	    return self._usage