import maya.cmds as cmds


def breakCon(obj=None, attr=None):
    if not obj:
        obj = cmds.ls(sl=True, fl=True)

    if isinstance(obj, str) or isinstance(obj, unicode):
        obj = [obj]

    for o in obj:
        conPairs = []
        try:
            con = cmds.listConnections(o, plugs=True, connections=True, destination=False)
            if con:
                conPairs.extend(zip(con[1::2], con[::2]))

            for source, dest in conPairs:
                if attr:
                    fullAttr = o + attr
                    if dest == fullAttr:
                        cmds.disconnectAttr(source, dest)
                else:
                    cmds.disconnectAttr(source, dest)
        except:
            pass


def unlockAttr(obj=None, attrList=None):
    if not obj:
        obj = cmds.ls(sl=True, fl=True)

    if isinstance(obj, str) or isinstance(obj, unicode):
        obj = [obj]

    if not attrList:
        attrList = ['.tx', '.ty', '.tz',
                    '.rx', '.ry', '.rz',
                    '.sx', '.sy', '.sz',
                    '.visibility']

    for o in obj:
        for attr in attrList:
            fullAttr = o + attr
            try:
                cmds.setAttr(fullAttr, l=False, k=True)
            except:
                pass


def enabledLayer(obj=None):
    if not obj:
        obj = cmds.ls(sl=True, fl=True)

    if isinstance(obj, str) or isinstance(obj, unicode):
        obj = [obj]

    for o in obj:
        try:
            layers = cmds.listConnections(o, t='displayLayer')
            if layers:
                for layer in layers:
                    cmds.setAttr(layer + '.enabled', 0)
        except:
            pass


def setVis(obj=None):
    if not obj:
        obj = cmds.ls(sl=True, fl=True)

    if isinstance(obj, str) or isinstance(obj, unicode):
        obj = [obj]

    attrAll = {
        '.overrideEnabled': 1,
        '.overrideDisplayType': 0,
        '.overrideLevelOfDetail': 0,
        '.overrideShading': 1,
        '.overrideTexturing': 1,
        '.overridePlayback': 1,
        '.overrideVisibility': 1,
        '.visibility': 1,
        '.lodVisibility': 1,
        '.template': 0,
        '.hiddenInOutliner': 0,
        '.hideOnPlayback': 0
    }

    for o in obj:
        try:
            shapeNode = cmds.listRelatives(o, s=True)
            if shapeNode:
                for shape in shapeNode:
                    obj.append(shape)

            if cmds.objectType(o) == 'joint':
                try:
                    cmds.setAttr(o + '.drawStyle', 0)
                except:
                    pass

            for attr, value in attrAll.iteritems():
                try:
                    cmds.setAttr(o + attr, value)
                except:
                    pass
        except:
            pass


@timeInfo
def build(obj=None):
    if not obj:
        obj = cmds.ls(sl=True, fl=True)

    if isinstance(obj, str) or isinstance(obj, unicode):
        obj = [obj]

    child = cmds.listRelatives(obj, ad=True)

    unlockAttr(child)
    breakCon(child, attr='.visibility')
    enabledLayer(child)
    setVis(child)
