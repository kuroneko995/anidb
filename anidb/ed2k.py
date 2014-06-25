import hashlib

class Ed2k:
    ''' Code taken from http://pydoc.net/Python/pyanidb/0.2.0/pyanidb.hash/
    and modified
    '''
    def __init__(self):
        self.md4_partial = hashlib.new('md4')
        self.md4_final = hashlib.new('md4')
        self.size_total = 0
	
    def update(self, data):
        pos = 0
        while pos < len(data):
            if (not (self.size_total % 9728000)) and self.size_total:
                self.md4_final.update(self.md4_partial.digest())
                self.md4_partial = hashlib.new('md4')
            size = min(len(data) - pos, 9728000 - (self.size_total % 9728000))
            self.md4_partial.update(data[pos:pos + size])
            pos += size
            self.size_total += size

    def hexdigest(self):
        if self.size_total > 9728000:
            self.md4_final.update(self.md4_partial.digest())
            return self.md4_final.hexdigest()
        return self.md4_partial.hexdigest()

        
