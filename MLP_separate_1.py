#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: mashutian
@time: 2019-03-10 13:25
@desc:
"""
from __future__ import print_function
# import sys
# sys.path.append("..") #if you want to import python module from other folders,
# you need to append the system path
import tensorflow as tf
from numpy.random import RandomState
from tensorflow.contrib.layers.python.layers import batch_norm as batch_norm  # for batch normalization
import numpy as np


class Config(object):
    def __init__(self, args):
        self.LAYER1_DIM = args.layer1_dim
        self.LAYER2_DIM = args.layer2_dim
        self.LAYER3_DIM = args.layer3_dim
        self.LAYER4_DIM = args.layer4_dim
        self.LEARNING_RATE = args.learning_rate
        self.EPOCH = args.epoch
        self.BATCH_SIZE = args.batch_size


class CitationRecNet(object):
    def __init__(self, layer1_dim, layer2_dim, layer3_dim, layer4_dim, x_dim1, x_dim2,
                 y_dim, learning_rate, data_num):
        # in order to generate same random sequences
        tf.set_random_seed(1)

        """
        input parameter
        """
        # 否则传不到MLP() 里面，要不然MLP() function 得写成MLP(layer1_dim) 的形式

        self.layer1_dim = layer1_dim
        self.layer2_dim = layer2_dim
        self.layer3_dim = layer3_dim
        self.layer4_dim = layer4_dim
        self.x_dim1 = x_dim1
        self.x_dim2 = x_dim2
        self.y_dim = y_dim
        self.learning_rate = learning_rate
        self.data_num = data_num

        """
        input data
        """
        # training data: record and label
        self.dropout_keep = tf.placeholder(dtype=tf.float32, name='dropout_keep')
        self.xa = tf.placeholder(tf.float32, shape=(None, self.x_dim1), name='xa-input')
        self.xb = tf.placeholder(tf.float32, shape=(None, self.x_dim2), name='xb-input')
        self.y = tf.placeholder(tf.float32, shape=(None, self.y_dim), name='y-input')
        """
        batch norm
        """
        # if self.is_batch_norm:
        #     update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
        #     with tf.control_dependencies(update_ops):
        #         self.loss = -tf.reduce_mean(self.y * tf.log(tf.clip_by_value(self.y_pred, 1e-10, 1.0)))
        #         self.loss = self.loss + tf.add_n(tf.get_collection('loss')) #L2 regularization
        # else:
        #     self.loss = -tf.reduce_mean(self.y * tf.log(tf.clip_by_value(self.y_pred, 1e-10, 1.0)))
        #     self.loss = self.loss + tf.add_n(tf.get_collection('loss')) #L2 regularization

        """
        graph structure
        """
        # predict data: label
        self.y_pred = self.MLP()
        self.y_pred_softmax = tf.nn.softmax(self.y_pred)
        # print(self.y_pred_softmax)

        # acc
        self.acc = tf.equal(tf.argmax(self.y_pred_softmax, 1), tf.argmax(self.y, 1))
        self.acc = tf.reduce_mean(tf.cast(self.acc, tf.float32))
        """
        model training 
        """
        self.loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.y_pred, labels=self.y))
        self.loss_metric = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.y_pred, labels=self.y))
        # self.loss = -tf.reduce_mean(self.y * tf.log(tf.clip_by_value(self.y_pred_softmax, 1e-10, 1.0)))
        # self.loss = tf.losses.mean_squared_error(self.y, self.y_pred_softmax)
        # self.loss = tf.reduce_mean(tf.square(self.y - self.y_pred_softmax))

        # loss_less = 10
        # loss_more = 0.1
        # self.loss = tf.reduce_sum(tf.where(tf.greater(self.y_pred_softmax, self.y),
        # (self.y_pred_softmax-self.y) * loss_more, (self.y-self.y_pred_softmax) * loss_less))

        # optimizer
        self.optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate, name='optimizer')
        # self.optimizer = tf.train.RMSPropOptimizer(learning_rate=self.learning_rate,
        #                                            decay=0.9, momentum=0.0, epsilon=1e-5, name='optimizer')

        # self.optimizer = tf.train.AdadeltaOptimizer(learning_rate=self.learning_rate, name='optimizer')
        # self.optimizer = tf.train.AdagradOptimizer(learning_rate=self.learning_rate, name='optimizer')
        # self.optimizer = tf.train.FtrlOptimizer(learning_rate=self.learning_rate, name='optimizer')
        # self.optimizer = tf.train.GradientDescentOptimizer(learning_rate=self.learning_rate, name='optimizer')
        # self.optimizer = tf.train.MomentumOptimizer(learning_rate=self.learning_rate, momentum=0.5, name='optimizer')
        # self.optimizer = tf.train.ProximalAdagradOptimizer(learning_rate=self.learning_rate, name='optimizer')
        # self.optimizer = tf.train.ProximalGradientDescentOptimizer(learning_rate=self.learning_rate, name='optimizer')

        self.train_op = self.optimizer.minimize(self.loss, name='train_op')

    def MLP(self):
        # network parameter
        # 问题：这里需要加self吗？比如下面这行
        # [x_dim, self.layer1_dim]这两个
        with tf.variable_scope("layer1"):
            self.W11 = tf.get_variable("w11", initializer=tf.random_normal([self.x_dim1, self.layer1_dim], stddev=0.1),
                                      dtype=tf.float32)
            self.W12 = tf.get_variable("w12", initializer=tf.random_normal([self.x_dim2, self.layer1_dim], stddev=0.1),
                                      dtype=tf.float32)
            self.b11 = tf.get_variable("b11", initializer=tf.zeros([self.layer1_dim]), dtype=tf.float32)
            self.b12 = tf.get_variable("b12", initializer=tf.zeros([self.layer1_dim]), dtype=tf.float32)


        with tf.variable_scope("layer2"):
            self.W21 = tf.get_variable("w21",
                                      initializer=tf.random_normal([self.layer1_dim, self.layer2_dim], stddev=0.1),
                                      dtype=tf.float32)
            self.W22 = tf.get_variable("w22",
                                      initializer=tf.random_normal([self.layer1_dim, self.layer2_dim], stddev=0.1),
                                      dtype=tf.float32)
            self.b21 = tf.get_variable("b21", initializer=tf.zeros([self.layer2_dim]), dtype=tf.float32)
            self.b22 = tf.get_variable("b22", initializer=tf.zeros([self.layer2_dim]), dtype=tf.float32)

        with tf.variable_scope("layer3"):
            self.W3 = tf.get_variable("w3",
                                      initializer=tf.random_normal([self.layer2_dim*2, self.layer3_dim], stddev=0.1),
                                      dtype=tf.float32)
            self.b3 = tf.get_variable("b3", initializer=tf.zeros([self.layer3_dim]), dtype=tf.float32)

        with tf.variable_scope("layer4"):
            self.W4 = tf.get_variable("w4",
                                      initializer=tf.random_normal([self.layer3_dim, self.layer4_dim], stddev=0.1),
                                      dtype=tf.float32)
            self.b4 = tf.get_variable("b4", initializer=tf.zeros([self.layer4_dim]), dtype=tf.float32)

        with tf.variable_scope("output"):
            self.W5 = tf.get_variable("w_output",
                                      initializer=tf.random_normal([self.layer3_dim, self.y_dim], stddev=0.1),
                                      dtype=tf.float32)

        # hidden1 = tf.nn.relu(tf.matmul(self.xa, self.W11) + tf.matmul(self.xb, self.W12) + self.b1)

        hidden11 = tf.nn.sigmoid(tf.matmul(self.xa, self.W11) + self.b11)
        hidden12 = tf.nn.sigmoid(tf.matmul(self.xb, self.W12) + self.b12)

        hidden11_drop = tf.nn.dropout(hidden11, self.dropout_keep)
        hidden12_drop = tf.nn.dropout(hidden12, self.dropout_keep)

        hidden21 = tf.nn.selu(tf.matmul(hidden11_drop, self.W21) + self.b21)
        hidden22 = tf.nn.selu(tf.matmul(hidden12_drop, self.W22) + self.b22)

        hidden21_drop = tf.nn.dropout(hidden21, self.dropout_keep)
        hidden22_drop = tf.nn.dropout(hidden22, self.dropout_keep)

        # hidden3 = tf.nn.sigmoid(tf.matmul(hidden21_drop+hidden22_drop, self.W3) + self.b3)
        hidden3 = tf.nn.sigmoid(tf.matmul(tf.concat([hidden21_drop, hidden22_drop], axis=1), self.W3) + self.b3)
        hidden3_drop = tf.nn.dropout(hidden3, self.dropout_keep)

        # hidden4 = tf.nn.relu(tf.matmul(hidden3_drop, self.W4) + self.b4)
        # hidden4_drop = tf.nn.dropout(hidden4, self.dropout_keep)

        y_pred = tf.matmul(hidden3_drop, self.W5)  # + self.b4
        return y_pred

    def CNN(self):
        pass



