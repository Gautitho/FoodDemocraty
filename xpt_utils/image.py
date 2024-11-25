# Standard / external libraries
import os
import PIL.Image
import PIL.PngImagePlugin
import piexif

# External modules

# Internal modules
import xpt_utils

###########################################
# Generic functions
###########################################

def get_tag_list_from_image(file_path):
  name = os.path.split(file_path)[-1]
  extension = name.split(".")[-1].lower()
  if (extension in ["png"]):
    tag_list = get_tag_list_from_png(file_path)
  elif (extension in ["jpg", "jpeg"]):
    tag_list = get_tag_list_from_jpg(file_path)
  else:
    raise xpt_utils.DevException(f"Extension ({extension}) of file {file_path} is not supported ! [image.get_tag_list_from_image]")
  return tag_list

def add_tag_list_to_image(file_path, new_tag_list):
  name = os.path.split(file_path)[-1]
  extension = name.split(".")[-1].lower()
  if (extension in ["png"]):
    add_tag_list_to_png(file_path, new_tag_list)
  elif (extension in ["jpg", "jpeg"]):
    add_tag_list_to_jpg(file_path, new_tag_list)
  else:
    raise xpt_utils.DevException(f"Extension ({extension}) of file {file_path} is not supported ! [image.add_tag_list_to_image]")

def remove_tag_list_from_image(file_path, rm_tag_list):
  name = os.path.split(file_path)[-1]
  extension = name.split(".")[-1].lower()
  if (extension in ["png"]):
    remove_tag_list_from_png(file_path, rm_tag_list)
  elif (extension in ["jpg", "jpeg"]):
    remove_tag_list_from_jpg(file_path, rm_tag_list)
  else:
    raise xpt_utils.DevException(f"Extension ({extension}) of file {file_path} is not supported ! [image.remove_tag_list_from_image]")


###########################################
# PNG functions
###########################################

def get_tag_list_from_png(file_path):
  tag_list = []

  img = PIL.Image.open(file_path)

  if ("tag_list" in img.info):
    tag_list = img.info["tag_list"].split(";")
    tag_list = list(dict.fromkeys(tag_list)) # Removing duplicates
    tag_list = list(filter(None, tag_list)) # Removing empty strings

  return tag_list

def add_tag_list_to_png(file_path, new_tag_list):
  img = PIL.Image.open(file_path)
  metadata = PIL.PngImagePlugin.PngInfo()
  tag_list = []
  for k in list(img.info.keys()):
    if (k == "tag_list"):
      tag_list = img.info[k].split(";")
    else:
      metadata.add_text(k, str(img.info[k]))
  tag_list.extend(new_tag_list)
  tag_list = list(dict.fromkeys(tag_list)) # Removing duplicates
  tag_list = list(filter(None, tag_list)) # Removing empty strings
  metadata.add_text("tag_list", ";".join(tag_list))
  img.save(file_path, pnginfo=metadata)

def remove_tag_list_from_png(file_path, rm_tag_list):
  img = PIL.Image.open(file_path)
  metadata = PIL.PngImagePlugin.PngInfo()
  tag_list = []
  for k in list(img.info.keys()):
    if (k == "tag_list"):
      tag_list = img.info[k].split(";")
    else:
      metadata.add_text(k, str(img.info[k]))
  for rm_tag in rm_tag_list:
    try:
      tag_list.remove(rm_tag)
    except:
      raise xpt_utils.DevException(f"Tag ({rm_tag}) could not be removed of file {file_path} because it doesn't exist ! [image.remove_tag_list_from_png]")
  metadata.add_text("tag_list", ";".join(tag_list))
  img.save(file_path, pnginfo=metadata)


###########################################
# JPG functions
###########################################

def get_tag_list_from_jpg(file_path):
  img = PIL.Image.open(file_path)
  tag_list = []

  if ("exif" in img.info):
    exif_dict = piexif.load(img.info["exif"])
    if (piexif.ImageIFD.XPKeywords in exif_dict["0th"]):
      # Getting the tag field of exif standard
      ascii_tag_tuple = exif_dict["0th"][piexif.ImageIFD.XPKeywords]
  
      # Interpreting tuple to extract a list of string
      tag = ""
      for el in list(ascii_tag_tuple):
        if (chr(el) == ";"):    # Tags are separated by ;
          tag_list.append(tag)
          tag = ""
        elif (el != 0):         # There is a dummy 0 between each character to remove
          tag += chr(el)
      tag_list.append(tag)
      tag_list = list(filter(None, tag_list)) # Removing empty strings

  return tag_list

def add_tag_list_to_jpg(file_path, new_tag_list):
  img = PIL.Image.open(file_path)
  tag_list = []

  if ("exif" in img.info):
    exif_dict = piexif.load(img.info["exif"])
    if (piexif.ImageIFD.XPKeywords in exif_dict["0th"]):
      # Getting the tag field of exif standard
      ascii_tag_tuple = exif_dict["0th"][piexif.ImageIFD.XPKeywords]
  
      # Interpreting tuple to extract a list of string
      tag = ""
      for el in list(ascii_tag_tuple):
        if (chr(el) == ";"):    # Tags are separated by ;
          tag_list.append(tag)
          tag = ""
        elif (el != 0):         # There is a dummy 0 between each character to remove
          tag += chr(el)
      tag_list.append(tag)
  else:
    exif_dict = {"0th" : {}}
  
  # Adding new tags to existing tags
  tag_list.extend(new_tag_list)
  tag_list = list(dict.fromkeys(tag_list)) # Removing duplicates
  tag_list = list(filter(None, tag_list)) # Removing empty strings

  # Formatting tag list in exif format ascii with 0 between each character (; as tag separator)
  ascii_tag_list = []
  for tag in tag_list:
    for c in tag:
      ascii_tag_list.extend([ord(c), 0])
    ascii_tag_list.extend([ord(";"), 0])
  ascii_tag_list.extend([0, 0]) # End of tag field

  # Adding new exif to the file
  exif_dict["0th"][piexif.ImageIFD.XPKeywords] = tuple(ascii_tag_list)
  exif_bytes = piexif.dump(exif_dict)
  img.save(file_path, "jpeg", exif=exif_bytes)

def remove_tag_list_from_jpg(file_path, rm_tag_list):
  img = PIL.Image.open(file_path)
  tag_list = []

  # Getting the tag field of exif standard
  if ("exif" in img.info):
    exif_dict = piexif.load(img.info["exif"])
    if (piexif.ImageIFD.XPKeywords in exif_dict["0th"]):
      ascii_tag_tuple = exif_dict["0th"][piexif.ImageIFD.XPKeywords]
  
      # Interpreting tuple to extract a list of string
      tag = ""
      for el in list(ascii_tag_tuple):
        if (chr(el) == ";"):    # Tags are separated by ;
          tag_list.append(tag)
          tag = ""
        elif (el != 0):         # There is a dummy 0 between each character to remove
          tag += chr(el)
      tag_list.append(tag)
      tag_list = list(filter(None, tag_list)) # Removing empty strings
  else:
    exif_dict = {"0th" : {}}
  
  # Removing desired tags
  for rm_tag in rm_tag_list:
    try:
      tag_list.remove(rm_tag)
    except:
      raise DevException(f"Tag ({rm_tag}) could not be removed of file {file_path} because it doesn't exist ! [image.remove_tag_list_from_png]")

  if (len(tag_list) > 0):
    # Formatting tag list in exif format ascii with 0 between each character (; as tag separator)
    ascii_tag_list = []
    for tag in tag_list:
      for c in tag:
        ascii_tag_list.extend([ord(c), 0])
      ascii_tag_list.extend([ord(";"), 0])
    ascii_tag_list.extend([0, 0]) # End of tag field

    # Adding new exif to the file
    exif_dict["0th"][piexif.ImageIFD.XPKeywords] = tuple(ascii_tag_list)
    exif_bytes = piexif.dump(exif_dict)
    img.save(file_path, "jpeg", exif=exif_bytes)