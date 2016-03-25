# -*- coding:utf-8 -*-
from flask import json
from kazoo.client import KazooClient
from kazoo.recipe.watchers import ChildrenWatch, DataWatch

__author__ = 'ylq'


class ClusterZookeeper(object):
    def __init__(self, zookeeper_hosts):
        self.groups_dict = {}
        self.topics_dict = {}
        self.brokers_list = []
        self.zk = KazooClient(hosts=zookeeper_hosts)
        self.zk.add_listener(self.keep_start)
        self.zk.start()
        if self.zk.exists('/consumers') is None or self.zk.exists('/brokers') is None:
            raise ValueError(zookeeper_hosts + 'is not zookeeper of kafka')
        ChildrenWatch(self.zk, '/consumers', self.groups_watch)
        ChildrenWatch(self.zk, '/brokers/topics', self.topics_watch)
        ChildrenWatch(self.zk, '/brokers/ids/', self.brokers_watch)

    # 保证链接是可用的
    def keep_start(self, client_status):
        print client_status
        if client_status != 'CONNECTED':
            try:
                self.zk.start()
            except():
                pass

    # 监听consumers节点
    def groups_watch(self, children):
        for group in [group for group in self.groups_dict.keys() if group not in children]:
            self.groups_dict.pop(group)
        for group in [group for group in children if group not in self.groups_dict.keys()]:
            owners_p = '/consumers/' + group + '/owners'
            if self.zk.exists(owners_p) is None:
                continue
            g_o_t = GroupOwnersTopic()
            self.groups_dict[group] = g_o_t
            ChildrenWatch(self.zk, owners_p, g_o_t.g_topic_watch)

    # 监听topic节点
    def topics_watch(self, children):
        for topic in [topic for topic in self.topics_dict.keys() if topic not in children]:
            self.topics_dict.pop(topic)
        for topic in [topic for topic in children if topic not in self.topics_dict.keys()]:
            t_v = TopicValue()
            self.topics_dict[topic] = t_v
            DataWatch(self.zk, '/brokers/topics/' + topic, t_v.topic_watch)

    # 监听broker节点
    def brokers_watch(self, children):
        self.brokers_list = children

    def close_zk(self):
        try:
            self.zk.remove_listener(self.keep_start)
            self.zk.stop()
            self.zk.close()
        except():
            pass


class GroupOwnersTopic(object):
    def __init__(self):
        self.topics_list = []

    def g_topic_watch(self, children):
        self.topics_list = children


class TopicValue(object):
    def __init__(self):
        self.topic_value = None

    def topic_watch(self, data, stat):
        self.topic_value = json.loads(data)["partitions"]


if __name__ == '__main__':
    zk_test = KazooClient(hosts='192.168.5.159:2181,192.168.5.159:2182,192.168.5.159:2183')
    zk_test.start()
    tops = zk_test.get_children('/brokers/topics/')
    print len(tops)
