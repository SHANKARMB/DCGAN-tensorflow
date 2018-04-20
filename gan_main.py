import os
import scipy.misc
import numpy as np

from model import DCGAN
from utils import pp, visualize, to_json, show_all_variables
import tensorflow as tf

# base_dir = "/content/training/"
base_dir = "/home/prime/ProjectWork/training/"
# base_dir = '/home/cprmi01/FinalSemProject/training'

flags = tf.app.flags
flags.DEFINE_float("learning_rate", 0.0002, "Learning rate of for adam [0.0002]")
flags.DEFINE_float("beta1", 0.5, "Momentum term of adam [0.5]")
flags.DEFINE_float("train_size", np.inf, "The size of train images [np.inf]")
flags.DEFINE_string("input_fname_pattern", "*.jpg", "Glob pattern of filename of input images [*]")
flags.DEFINE_string("sample_dir", "samples", "Directory name to save the image samples [samples]")
flags.DEFINE_boolean("train", False, "True for training, False for testing [False]")
flags.DEFINE_boolean("crop", False, "True for training, False for testing [False]")
flags.DEFINE_boolean("visualize", False, "True for visualizing, False for nothing [False]")

# changed
flags.DEFINE_integer("epoch", 5000, "Epoch to train [25]")
flags.DEFINE_integer("batch_size", 32, "The size of batch images [64]")
flags.DEFINE_integer("input_height", 256, "The size of image to use (will be center cropped). [108]")
flags.DEFINE_integer("input_width", 256,
                     "The size of image to use (will be center cropped). If None, same value as input_height [None]")
flags.DEFINE_integer("output_height", 256, "The size of the output images to produce [64]")
flags.DEFINE_integer("output_width", 256,
                     "The size of the output images to produce. If None, same value as output_height [None]")
flags.DEFINE_integer("num_classes", 10, "Number of classes to train on. [100]")
flags.DEFINE_integer("generate_test_images", 2, "Number of images to generate during test. [100]")
flags.DEFINE_string("checkpoint_dir", "trained/gan/", "Directory name to save the checkpoints [checkpoint]")
flags.DEFINE_string("dataset_dir", "dataset/gan_files/", "Dataset dir where data is in 'dataset' dir")
flags.DEFINE_string("dataset", "images101", "The name of dataset [images10,celebA, mnist, lsun]")
flags.DEFINE_string("base_dir", "/home/prime/ProjectWork/training/", "base dir")

FLAGS = flags.FLAGS


def train_gan(learning_rate=0.0002, input_width=256, input_height=256,
              output_width=256, output_height=256, checkpoint_dir="trained/gan/",
              sample_dir='samples', dataset='images10', batch_size=32,
              num_classes=10, generate_test_images=5,
              input_fname_pattern='*.jpg', dataset_dir='dataset/gan_files/',
              crop=False, train=True
              ):
    print('started')
    FLAGS.learning_rate = learning_rate
    FLAGS.input_width = input_width
    FLAGS.input_height = input_height
    FLAGS.output_width = output_width
    FLAGS.output_height = output_height
    FLAGS.checkpoint_dir = checkpoint_dir
    FLAGS.sample_dir = sample_dir
    FLAGS.dataset = dataset
    FLAGS.batch_size = batch_size
    FLAGS.num_classes = num_classes
    FLAGS.generate_test_images = generate_test_images
    FLAGS.input_fname_pattern = input_fname_pattern
    FLAGS.dataset_dir = dataset_dir
    FLAGS.crop = crop
    FLAGS.train = train
    tf.app.run(main=main)


def test_gan(learning_rate=0.0002, input_width=256, input_height=256,
             output_width=256, output_height=256, checkpoint_dir="trained/gan/",
             sample_dir='samples', dataset='images10', batch_size=32,
             num_classes=10, generate_test_images=5,
             input_fname_pattern='*.jpg', dataset_dir='dataset/gan_files/',
             crop=False, train=False
             ):
    FLAGS.learning_rate = learning_rate
    FLAGS.input_width = input_width
    FLAGS.input_height = input_height
    FLAGS.output_width = output_width
    FLAGS.output_height = output_height
    FLAGS.checkpoint_dir = checkpoint_dir
    FLAGS.sample_dir = sample_dir
    FLAGS.dataset = dataset
    FLAGS.batch_size = batch_size
    FLAGS.num_classes = num_classes
    FLAGS.generate_test_images = generate_test_images
    FLAGS.input_fname_pattern = input_fname_pattern
    FLAGS.dataset_dir = dataset_dir
    FLAGS.crop = crop
    FLAGS.train = train
    print('train', FLAGS.train)
    tf.app.run(main=main)


def main(_):
    pp.pprint(flags.FLAGS.__flags)
    base_dir = FLAGS.base_dir
    if FLAGS.input_width is None:
        FLAGS.input_width = FLAGS.input_height
    if FLAGS.output_width is None:
        FLAGS.output_width = FLAGS.output_height

    if not os.path.exists(os.path.join(base_dir, FLAGS.checkpoint_dir)):
        os.makedirs(os.path.join(base_dir, FLAGS.checkpoint_dir))
    if not os.path.exists(FLAGS.sample_dir):
        os.makedirs(FLAGS.sample_dir)

    # gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.333)
    run_config = tf.ConfigProto()
    run_config.gpu_options.allow_growth = True
    # print('Training: ',FLAGS.train)
    with tf.Session(config=run_config) as sess:
        if FLAGS.dataset == 'mnist':
            dcgan = DCGAN(
                sess,
                input_width=FLAGS.input_width,
                input_height=FLAGS.input_height,
                output_width=FLAGS.output_width,
                output_height=FLAGS.output_height,
                batch_size=FLAGS.batch_size,
                sample_num=FLAGS.batch_size,
                y_dim=FLAGS.num_classes,
                z_dim=FLAGS.generate_test_images,
                dataset_name=FLAGS.dataset,
                input_fname_pattern=FLAGS.input_fname_pattern,
                crop=FLAGS.crop,
                checkpoint_dir=FLAGS.checkpoint_dir,
                sample_dir=FLAGS.sample_dir

            )
        elif FLAGS.dataset == 'images10':
            dcgan = DCGAN(
                sess,
                input_width=FLAGS.input_width,
                input_height=FLAGS.input_height,
                output_width=FLAGS.output_width,
                output_height=FLAGS.output_height,
                batch_size=FLAGS.batch_size,
                sample_num=FLAGS.batch_size,
                y_dim=FLAGS.num_classes,
                z_dim=FLAGS.generate_test_images,
                dataset_name=FLAGS.dataset,
                input_fname_pattern=FLAGS.input_fname_pattern,
                crop=FLAGS.crop,
                checkpoint_dir=FLAGS.checkpoint_dir,
                sample_dir=FLAGS.sample_dir,
                dataset_dir=FLAGS.dataset_dir

            )
        else:
            dcgan = DCGAN(
                sess,
                input_width=FLAGS.input_width,
                input_height=FLAGS.input_height,
                output_width=FLAGS.output_width,
                output_height=FLAGS.output_height,
                batch_size=FLAGS.batch_size,
                sample_num=FLAGS.batch_size,
                z_dim=FLAGS.generate_test_images,
                dataset_name=FLAGS.dataset,
                input_fname_pattern=FLAGS.input_fname_pattern,
                crop=FLAGS.crop,
                checkpoint_dir=FLAGS.checkpoint_dir,
                sample_dir=FLAGS.sample_dir,
                dataset_dir=FLAGS.dataset_dir
            )

        show_all_variables()
        print('going to train')
        if FLAGS.train:
            dcgan.train(FLAGS)
        else:
            if not dcgan.load(FLAGS.checkpoint_dir)[0]:
                raise Exception("[!] Train a model first, then run test mode")

        # to_json("./web/js/layers.js", [dcgan.h0_w, dcgan.h0_b, dcgan.g_bn0],
        #                 [dcgan.h1_w, dcgan.h1_b, dcgan.g_bn1],
        #                 [dcgan.h2_w, dcgan.h2_b, dcgan.g_bn2],
        #                 [dcgan.h3_w, dcgan.h3_b, dcgan.g_bn3],
        #                 [dcgan.h4_w, dcgan.h4_b, None])

        # Below is codes for visualization
        OPTION = 1
        visualize(sess, dcgan, FLAGS, OPTION)


if __name__ == '__main__':
    tf.app.run()