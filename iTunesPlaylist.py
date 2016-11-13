import plistlib

class iTunesPlaylist:
    '''
    Class for processing iTunes playlist
    '''

    def __init__(self, fileName):
        #dictionary - trackName: {'Duration': duration, 'Count': count}        self.tracks = {}
        self.tracks = {}

        #load playlist from file
        ptracks = self.loadPlaylist(fileName)
        self.getTracksFromPlaylist(ptracks)

    def loadPlaylist(self, fileName):
        # open file for read binary
        with open(fileName, 'rb') as fp:
            plist = plistlib.load(fp)

        ptracks = plist['Tracks']

        return ptracks

    def getTracksFromPlaylist(self, ptracks):
        for trackId, track in ptracks.items():
            try:
                name = track['Name']
                duration = track['Total Time']

                #check if duplicate
                if name in self.tracks:
                    if duration // 1000 == self.tracks[name]['Duration'] // 1000:
                        count = self.tracks[name]['Count']
                        self.tracks[name] = {'Duration': duration,
                                             'Count': count + 1}
                else:
                    self.tracks[name] = {'Duration': duration,
                                         'Count': 1}
            except:
                pass

    def findDuplicates(self, fileName):
        duplicates = {}

        for name, track in self.tracks:
            if track['Count'] > 1:
                duplicates[name] = track

        return duplicates

    def writeDuplicates(self, fileName, duplicates):
        if len(duplicates) > 0:
            print('Find %d duplicates. '
                  'Write songs names to file %s'
                  % (len(duplicates), fileName))
        else:
            print('No duplicates found!')

        # write duplicates to file
        f = open(fileName, 'w')

        for key, val in duplicates.items():
            f.write('[%d] %s\n' % (val['Count'], key))

        f.close()