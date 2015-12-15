import xml.dom.minidom

class Task:
    def __init__(self, id, time, processor, num):
        self.id = id
        self.time = time
        self.processor = processor
        self.num = num

class Link:
    def __init__(self, src, dst, vol):
        self.src = src
        self.dst = dst
        self.vol = vol

class Schedule:
    def __init__(self):
        self.tasks = []
        self.links = []

    def exportXML(self, filename):
        dom = xml.dom.minidom.Document()
        root = dom.createElement("schedule")
        dom.appendChild(root)
        for t in self.tasks:
            task = dom.createElement("task")
            task.setAttribute("id", t.id)
            task.setAttribute("time", str(t.time))
            task.setAttribute("num", str(t.num))
            task.setAttribute("processor", t.processor)
            root.appendChild(task)
        for l in self.links:
            link = dom.createElement("link")
            link.setAttribute("src", l.src)
            link.setAttribute("dst", l.dst)
            link.setAttribute("vol", str(l.vol))
            root.appendChild(link)
        f = open(filename, "w")
        f.write(dom.toprettyxml())
        f.close()

