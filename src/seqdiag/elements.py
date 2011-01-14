#!bin/py
# -*- coding: utf-8 -*-

import re
import sys
import blockdiag.elements
from blockdiag.elements import *
from blockdiag.utils.XY import XY


class DiagramNode(blockdiag.elements.DiagramNode):
    def __init__(self, id):
        blockdiag.elements.DiagramNode.__init__(self, id)

        self.activity = []
        self.activities = []

    def activate(self, height, index):
        if len(self.activity) <= index:
            self.activity.insert(index, [])

        if len(self.activity[index]) > 0 and \
           self.activity[index][-1] != height - 1:
            self.deactivate(index)

        self.activity[index].append(height)

    def deactivate(self, index=None):
        if index is None:
            for i in range(len(self.activity)):
                self.deactivate(i)
            return

        if self.activity[index]:
            attr = {'lifetime': self.activity[index],
                    'level': index}
            self.activities.append(attr)

        self.activity[index] = []


class DiagramEdge(blockdiag.elements.DiagramEdge):
    return_label = None

    def __init__(self, node1, node2):
        blockdiag.elements.DiagramEdge.__init__(self, node1, node2)

        self.height = 1
        self.y = 0
        self.async = False
        self.diagonal = False
        self.return_label = ''

    def setAttributes(self, attrs):
        attrs = list(attrs)
        for attr in list(attrs):
            value = unquote(attr.value)

            if attr.name == 'return':
                self.return_label = value
                attrs.remove(attr)
            elif attr.name == 'diagonal':
                self.diagonal = True
                self.height = 1.5
                attrs.remove(attr)
            elif attr.name == 'async':
                self.dir = 'forward'
                attrs.remove(attr)
            elif attr.name == 'dir':
                dir = value.lower()
                if dir in ('back', 'both', 'forward'):
                    self.dir = dir
                elif dir == '=>':
                    self.dir = 'both'
                elif dir in ('->', '->>', '-->', '-->>'):
                    self.dir = 'forward'

                    if re.search('--', dir):
                        self.style = 'dashed'
                    else:
                        self.style = None

                    if re.search('>>', dir):
                        self.async = True
                    else:
                        self.async = False
                elif dir in ('<-', '<<-', '<--', '<<--'):
                    self.dir = 'back'

                    if re.search('--', dir):
                        self.style = 'dashed'
                    else:
                        self.style = None

                    if re.search('<<', dir):
                        self.async = True
                    else:
                        self.async = False
                else:
                    msg = "WARNING: unknown edge dir: %s\n" % dir
                    sys.stderr.write(msg)

                attrs.remove(attr)

        blockdiag.elements.DiagramEdge.setAttributes(self, attrs)