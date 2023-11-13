import datetime
import sys



class Reporter():

    def __init__(self,file_name) -> None:
        self._results = []
        self._event_start_time = {}
        self._file_name = file_name

    def report(self) -> None:
        
        self._calculate()
        self._present()

        return None

    def _present(self) -> None:
        """give the output formatted"""
        offset = 29

        print(f"| {'Function Name'.ljust(offset,' ')}| {'Num. of calls'.ljust(offset,' ')}| {'Total Time (ms)'.ljust(offset,' ')}| {'Average Time (ms)'.ljust(offset,' ')}|")
        print(f"|{''.ljust(offset+1,'-')}|{''.ljust(offset+1,'-')}|{''.ljust(offset+1,'-')}|{''.ljust(offset+1,'-')}|")
        
        for result in self._results:
            func = result[0].ljust(offset," ")
            calls = str(result[1]).ljust(offset," ")
            total = str(result[2]).ljust(offset," ")
            average = str(result[3]).ljust(offset," ")
            print(f"| {func}| {calls}| {total}| {average}|")
        

        return None

    def _calculate(self) -> None:
        """calculate numebr of calls total runtime and average runtime"""
        total_call_time = {}
        #keys are id of functions, values are list with [name,no_calls,totaltime]

        with open(self._file_name,"r") as log_file:
            for log_line in log_file.readlines():
                log_info = log_line.strip().split(",")


                assert len(log_info) == 4, f"line has {len(log_info)} entries instead of 5"
                id, name, event, time = log_info

                if event == "start":
                    if id not in total_call_time.keys():
                        total_call_time[id] = [name,0,0]
                    total_call_time[id][1] += 1
                    self._set_start(id,time)

                elif event == "end":
                    end_time = datetime.datetime.strptime(time,'%Y-%m-%d %H:%M:%S.%f')
                    start_time = self._event_start_time[int(id)].pop()
                    start_time = time = datetime.datetime.strptime(start_time,'%Y-%m-%d %H:%M:%S.%f')
                    totaltime = (end_time - start_time).total_seconds()
                    total_call_time[id][2] += totaltime

        for id,info in total_call_time.items():
            info[2] = info[2]*1000
            info.append(info[2]/info[1])
            self._results.append(info)

        
                    

    def _set_start(self, id:str, time:datetime) -> None:
        """set starting times for a given id"""
        id = int(id)
        if id in self._event_start_time.keys():
            self._event_start_time[id].append(time)
        else:
            self._event_start_time[id] = [time]



def main():
    assert len(sys.argv) == 2, "bad usage try: python reporting.py <filename>"

    reporter = Reporter(sys.argv[1])
    try:
        reporter.report()
    except:
        raise Exception (f'the file {sys.argv[1]} does not exist')
    



if __name__ == "__main__":
    main()