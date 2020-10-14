from flask import Blueprint, request, render_template, abort, send_file, Response
from skimage.io import imsave
import numpy as np 
from . import main_tools
from .. import models
import json
import os
import io

main = Blueprint('main', __name__, template_folder='views')

@main.route('/upload_frame', methods=['POST'])
def upload():
    
    file_type = ''
    try: 
        file = request.files['Grayscale']
        file_type = 'Grayscale'
    except:
        print('wrong filetype')
    try:
        file = request.files['Pencil_Edge']
        file_type = 'Pencil_Edge'
    except:
        print('wrong filetype')
    try:
        file = request.files['Pencil_Sketch']
        file_type = 'Pencil_Sketch'
    except:
        print('wrong filetype')
    
    processed_img, processed_img_array = models.image_handler.Process_Frame(file, file_type)
    processed_img.save(os.path.join(os.getcwd(), 'tmp.png'))

    strIO = io.BytesIO()
    imsave(strIO, processed_img_array, plugin='pil', format_str='png')
    strIO.seek(0)
    
    return send_file(strIO, mimetype='image/png')
    
@main.route('/generate_image', methods=['GET'])
def generate_image():
    """
    Return a generated image as a png by
    saving it into a StringIO and using send_file.
    """
    num_tiles = 20
    tile_size = 30
    arr = np.random.randint(0, 255, (num_tiles, num_tiles, 3))
    arr = arr.repeat(tile_size, axis=0).repeat(tile_size, axis=1)

    # We make sure to use the PIL plugin here because not all skimage.io plugins
    # support writing to a file object.
    strIO = io.BytesIO()
    imsave(strIO, arr, plugin='pil', format_str='png')
    strIO.seek(0)
    models.image_handler.debug_test()
    return send_file(strIO, mimetype='image/png')

@main.route('/', methods=['GET'])
def test_client():
    return Response(json.dumps({'Output': 'Olympus application'}), mimetype='application/json', status=200)