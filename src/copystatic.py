import os
import shutil
import logging

logging.basicConfig(
    filename='copy_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def copy_content():
    working_dir = os.getcwd()
    public_dir = os.path.join(working_dir, "docs")
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
        logging.info(f"deleted directory: {public_dir}")
    os.mkdir(public_dir)
    logging.info(f"created directory: {public_dir}")
    static_dir = os.path.join(working_dir, "static")
    if os.path.exists(static_dir):
        logging.info("starting with copy process:")
        copy_content_helper(static_dir, public_dir)
        logging.info("copy process was successful")
    else:
        raise NotADirectoryError(static_dir)

def copy_content_helper(src_path, dst_path):
    files = os.listdir(src_path)
    for file in files:
        if os.path.isdir(os.path.join(src_path, file)):
            new_dst_path = os.path.join(dst_path, file)
            new_src_path = os.path.join(src_path, file)
            if not os.path.isfile(new_dst_path):
                os.mkdir(new_dst_path)
                logging.info(f"created directory: {new_dst_path}")
            copy_content_helper(new_src_path, new_dst_path)
        else:
            shutil.copy(os.path.join(src_path, file), dst_path)
            logging.info(f"copied: {src_path} to {dst_path}")