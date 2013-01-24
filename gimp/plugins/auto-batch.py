'''
The MIT License (MIT)
Copyright (c) 2013 Danny Crasto 

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

#!/usr/bin/env python

import math
import os
import time
import sys
import traceback
from distutils.dir_util import copy_tree
from gimpfu import *
''' 
    TODO
    * make it run w/o an image needing to be open
    * multithreaded
    * make output or input dir change default dir trigger
    * filter only image files
    * more granular/informative progress bar
'''
def getFileList( path, srcPath ):
    fileList = []
    dirList = []
    dirList.append( path )
    while len( dirList )  > 0 :
        curDir = dirList.pop()
        curlist = os.listdir( curDir )
        for f in curlist:
            fo = os.path.join( curDir, f )
            if os.path.isfile( fo ):
                fileList.append( fo )
            elif os.path.isdir( fo ) and not srcPath == fo:
                dirList.append( fo )
    return fileList

def auto_batch( white_balance, 
                auto_color, input_dir, output_dir ):
    
    if not input_dir == output_dir: 
        copy_tree( input_dir, output_dir )

    fileList = getFileList( output_dir, input_dir )
    gimp.progress_init( "Going to process %i files"%( len( fileList ) ) )
    count = 1.0
    total_count = len( fileList )
    for f in fileList:
        try:
            image    = pdb.gimp_file_load( f, f )
            drawable = pdb.gimp_image_get_active_drawable( image )

            if white_balance:
                pdb.gimp_levels_stretch( drawable )
            if auto_color:
                pdb.plug_in_autostretch_hsv( image, drawable )

            pdb.gimp_file_save( image, drawable, f, f )
            pdb.gimp_image_delete( image )
        except:
            pdb.gimp_message( "Failed to process '%s' : %s"%( f, traceback.format_exc() ) )


        gimp.progress_update( count / len( fileList ) )
        count = count + 1
    print "Finished"

register(
        "auto_batch",
        "Batch run auto correct filters",
        "Batch run auto correct filters",
        "Danny Crasto",
        "Danny Crasto",
        "2013",
        "<Toolbox>/_Xtns/_Auto Batch",
        "RGB*, GRAY*",
        [
            (PF_TOGGLE, "white_balance", "Apply Auto white balance", 1),
            (PF_TOGGLE, "auto_color", "Apply Auto color", 1),
            (PF_DIRNAME, "input_dir", "Input Directory", "~/"),
            (PF_DIRNAME, "output_dir", "Output Directory", "~/"),
        ],
        [],
        auto_batch)

main()
