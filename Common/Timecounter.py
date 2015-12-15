__author__ = 'alevtina'
__doc__ = 'Builds a state chart for schedule, runs it and ' \
          'finds execution times of tasks.'
import xml.dom.minidom, sys

class Task:
    def __init__(self, id, time, proc, num):
        self.proc = proc
        self.time = time
        self.id = id
        self.num = num
        self.state = "WAIT_DATA"
        self.previous_tasks = []
        self.output_links = []
        self.start_work_time = -1
        self.start_send_time = -1
        self.end_time = -1

class Link:
    def __init__(self, src, dst, vol):
        self.src = src
        self.dst = dst
        self.vol = vol
        self.start_time = -1
        self.transfer_finished = False

class Processor:
    def __init__(self, id):
        self.tasks = []
        self.id = id
        self.current_task = None

class System:
    def __init__(self):
        self.processors = []
        self.time = 0
        self.freeChannel = True

    def findTaskById(self,id):
        for p in self.processors:
            for t in p.tasks:
                if t.id == id:
                    return t

    def findLinkByDst(self, task, dst):
        for l in task.output_links:
            if l.dst == dst:
                return l

    def loadXML(self, filename):
        f = open(filename, "r")
        dom = xml.dom.minidom.parse(f)
        for task in dom.getElementsByTagName("task"):
            id = task.getAttribute("id")
            time = task.getAttribute("time")
            proc = task.getAttribute("processor")
            num = task.getAttribute("num")
            processor = None
            for p in self.processors:
                if p.id == proc:
                    processor = p
                    break
            if processor == None:
                processor = Processor(proc)
                self.processors.append(processor)
            processor.tasks.append(Task(id, int(time), proc, int(num)))
        for link in dom.getElementsByTagName("link"):
            src = link.getAttribute("src")
            dst = link.getAttribute("dst")
            vol = link.getAttribute("vol")
            link = Link(src, dst, int(vol))
            src_task = self.findTaskById(src)
            dst_task = self.findTaskById(dst)
            if src_task.proc == dst_task.proc:
                continue
            src_task.output_links.append(link)
            dst_task.previous_tasks.append(src_task)
        f.close()
        for p in self.processors:
            p.tasks.sort(key=lambda x: x.num)
            p.current_task = p.tasks[0]

    def allFinished(self):
        for p in self.processors:
            for t in p.tasks:
                if t.end_time == -1:
                    return False
        return True

    def dataReceived(self, task):
        for t in task.previous_tasks:
            link = self.findLinkByDst(t, task.id)
            if not link:
                print("Something went wrong")
                exit(1)
            if not link.transfer_finished:
                return False
        return True


    def work(self):
        while not self.allFinished():
            changed = False
            for p in self.processors:
                if not p.current_task:
                    continue
                if p.current_task.state == "WAIT_DATA":
                    if self.dataReceived(p.current_task):
                        p.current_task.state = "WORK"
                        p.current_task.start_work_time = self.time
                        changed = True
                elif p.current_task.state == "WORK":
                    if self.time - p.current_task.start_work_time == p.current_task.time:
                        p.current_task.state = "WAIT_CHANNEL"
                        changed = True
                elif p.current_task.state == "WAIT_CHANNEL":
                    if self.freeChannel:
                        p.current_task.state = "SEND"
                        p.current_task.start_send_time = self.time
                        self.freeChannel = False
                        changed = True
                elif p.current_task.state == "SEND":
                    if p.current_task.output_links == []:
                        p.current_task.state = "END"
                        self.freeChannel = True
                        changed = True
                    else:
                        if all(l.transfer_finished for l in p.current_task.output_links):
                            p.current_task.state = "END"
                            self.freeChannel = True
                            changed = True
                        else:
                            if p.current_task.output_links[0].start_time == -1:
                                p.current_task.output_links[0].start_time = self.time
                            for l in p.current_task.output_links:
                                if l.start_time != -1 and not l.transfer_finished and self.time - l.start_time == l.vol:
                                    l.transfer_finished = True
                                    changed = True
                                    idx = p.current_task.output_links.index(l)
                                    if idx != len(p.current_task.output_links) - 1:
                                        p.current_task.output_links[idx+1].start_time = self.time
                elif p.current_task.state == "END":
                    p.current_task.end_time = self.time
                    idx = p.tasks.index(p.current_task)
                    if idx != len(p.tasks)-1:
                        p.current_task = p.tasks[idx+1]
                        changed = True
                    else:
                        p.current_task = None
            if not changed:
                self.time += 1

    def exportXML(self, filename):
        f = open(filename, 'w')
        doc = xml.dom.minidom.Document()
        results = doc.createElement('results')
        doc.appendChild(results)
        for p in self.processors:
            for t in p.tasks:
                task = doc.createElement('task')
                task.setAttribute('id', t.id)
                task.setAttribute('processor', t.proc)
                task.setAttribute('time', str(t.end_time))
                results.appendChild(task)
        f.write(doc.toprettyxml())
        f.close()

if __name__ == "__main__":
    system = System()
    system.loadXML(sys.argv[1])
    system.work()
    system.exportXML(sys.argv[2])