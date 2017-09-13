
#License MIT 2017 Ahmad Retha

class Motif:
	def __init__(self):
		self.id = ''				#required
		self.altId = None			#optional
		self.letterProbability = {}	#required
		self.matrix = []			#required
		self.url = None				#optional		

class MEMEFile:
	def __init__(self, motif_file):
		self.version = None			#required
		self.alphabet = ''			#recommended
		self.strands = '-'			#optional
		self.backgroundSource = ''  #optional
		self.background = {}		#recommended
		self.motifs = []			#required
		self.errors = []
		self.parse(motif_file)

	def parse(self, motif_file):
		success = self.parseHead(motif_file)
		if not success:
			return False
		return self.parseRest(motif_file)

	def parseHead(self, motif_file):
		started = False
		inAlphabet = False
		inBackground = False
		i = 0

		for line in motif_file:
			line = line.strip()
			i += 1

			if line == '':
				if inBackground:
					inBackground = False
				if inAlphabet:
					inAlphabet = False
				continue

			if not started: 
				if not line.startswith('MEME version '):
					self.errors.append('Missing MEME Version')
					return False
				self.version = line[12:].lstrip()
				started = True
				continue

			if line.startswith('ALPHABET='):
				self.alphabet += line[9:].lstrip()
				inAlphabet = True
				continue

			if inAlphabet:
				if line.startswith('END ALPHABET'):
					inAlphabet = False
				else:
					self.alphabet += line
				continue

			if line.startswith('strands: '):
				self.strands = line[8:].lstrip()
				continue

			if line.startswith('Background letter frequencies'):
				if 'from ' in line:
					self.backgroundSource = line[36:-2].strip()
				inBackground = True
				continue

			if inBackground:
				ln = line.split()
				while ln:
					letter = ln.pop(0)
					freq = ln.pop(0)
					self.background[letter] = freq
				continue

			break

		motif_file.seek(0)
		while i > 1:
			motif_file.readline()
			i -= 1
		return True

	def parseRest(self, motif_file):
		motif = None
		inMatrix = False

		for line in motif_file:
			line = line.strip()

			if line == '':
				inMatrix = False
				continue

			if line.startswith('MOTIF '):
				if motif:
					self.motifs.append(motif)
				motif = Motif()
				ids = line[6:].split()
				motif.id = ids.pop(0)
				if ids:
					motif.altId = ids.pop(0)
				continue

			if line.startswith('letter-probability matrix: '):
				parts = line[27:].split()
				while parts:
					k = parts.pop(0)
					k = k[:-1].strip()
					v = parts.pop(0)
					v = v.strip()
					motif.letterProbability[k] = v
				inMatrix = True
				continue

			if inMatrix:
				motif.matrix.append([float(x) for x in line.split()])
				continue

			if line.startswith('URL '):
				inMatrix = False
				motif.url = line[4:].lstrip()
				continue

		self.motifs.append(motif)
		return True

