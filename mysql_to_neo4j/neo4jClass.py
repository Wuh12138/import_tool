import py2neo


class Neo4jOperation:
    """实现对neo4j关系与数据的增删改查"""
    __mgraph = 0
    __matcher = 0

    def __init__(self, key, name="neo4j", url='http://localhost:7474'):
        """

        :param key:密码
        :param name: 数据库名字
        :param url: 数据库访问地址
        """
        self.__mgraph = py2neo.Graph(url, auth=("neo4j", key), name=name)
        self.__matcher = py2neo.NodeMatcher(self.__mgraph)  # 创建关系需要用到

    @staticmethod
    def node(*labels, **properties):
        """

        :param labels: 节点标签
        :param properties: 节点属性
        :return: 返回节点对象,调用cr_node添加到图中
        """
        return py2neo.Node(*labels, **properties)

    def cr_node(self, node):
        """

        :param node: 待添加节点
        :return: 没有返回值
        """
        self.__mgraph.create(node)

    def add_node(self, *labels, **properties):
        """

        :param labels: 标签
        :param properties: 属性
        :return: 返回节点对象

        dd
        """
        n = py2neo.Node(*labels, **properties)
        self.__mgraph.create(n)
        return n

    def cr_relation(self, *node1, **properties):
        """

        :param node1: 前驱节点, ”关系“, 后继节点
        :param properties: 属性  eg: price=45
        :return: 关系对象
        """
        r = py2neo.Relationship(*node1, **properties)
        self.__mgraph.create(r)
        return r

    def delete_all(self):
        """

        :return: 删除所有节点和关系
        """
        self.__mgraph.delete_all()

    def foreach_node(self, function):
        """

        :param function: 喊一个参数的会掉函数
        :return: 对所有节点执行回调函数
        """
        index = self.__mgraph.nodes
        for i in index:
            function(index[i])

    def foreach_relation(self, function):
        """
        :param function: 含有一个关系对象作为参数的回调函数
        :return: 对所有关系执行回调函数
        """
        r = self.__mgraph.relationships
        for i in r:
            function(r[i])

    def match_node(self, *labels, **properties):
        """

        :param labels: 节点标签
        :param properties: 节点属性
        :return: 返回迭代器
        """
        return self.__mgraph.nodes.match(*labels, **properties)

    def match_relation(self, node, r_type, **properties):
        """

        :param node: 前驱节点,后继节点 node=(start,end)
        :param r_type: 关系标签
        :param properties: 关系属性
        :return: 可单独按照一个特征查,node或者r_type没有时, 使用None,返回迭代器
        """
        return self.__mgraph.relationships.match(node, r_type, **properties)

    def run_command(self, command: object) -> object:
        """
        :param command: 要执行的命令
        :return: 根据命令返回
        """
        try:
            return self.__mgraph.run('match(n:book{name:"内经"}) detach delete n')

        except:
            print(command + '  res:执行失败')

    def delete(self, sgraph):
        """删除节点或者关系"""
        self.__mgraph.delete(sgraph)

    def update_node(self, node, **kwargs):
        """
        更新节点属性
        :param node: 需要更新的节点
        :param kwargs: 更新的属性
        :return: 更新后的节点
        """
        for key, value in kwargs.items():
            node[key] = value
        self.__mgraph.push(node)
        return node

    def find_node_by_label(self, label):
        """
        根据标签查找节点
        :param label: 节点的标签
        :return: 查找到的节点列表
        """
        return list(self.__mgraph.nodes.match(label))

