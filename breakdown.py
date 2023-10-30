
with open("breakdown.txt", "r") as f:
    raw = f.readlines()
    # Procedure Name: [[ops], [ops time(ms)], {"msm": total time in milliseconds, "fft":..., "ifft":..., ("pairing":...)}, total time]
    components = {}
    curr_comp = ""
    parse_flag = False
    for line in raw:
        if line.strip() == "Start:   Prove":
            parse_flag = True
            curr_comp = "prove"
            components[curr_comp] = [[], [], {"msm": 0, "fft": 0, "ifft": 0}, 0]
        elif line.strip() == "Start:   Verify":
            parse_flag = True
            curr_comp = "verify"
            components[curr_comp] = [[], [], {"msm": 0, "fft": 0, "ifft": 0, "pairing": 0}, 0]
        elif parse_flag:
            elems = line.strip().split(".")
            if "End" in elems[0]:
                op = elems[0].split(" ")[-2]
                if "ms" in elems[-1]:
                    ti = float(elems[-2]+"."+elems[-1][:-2])
                elif "µs" in elems[-1]:
                    ti = float(elems[-2]+"."+elems[-1][:-2])/1000
                elif "ns" in elems[-1]:
                    ti = float(elems[-2]+"."+elems[-1][:-2])/1000000
                else:
                    ti = float(elems[-2]+"."+elems[-1][:-2]) * 1000 

                if "msm" in op or "fft" in op or "pairing" in op:
                    components[curr_comp][0].append(op)
                    components[curr_comp][1].append(ti)
                    components[curr_comp][2][op.split("-")[0]] += ti
                else:
                    parse_flag = False
                    components[curr_comp][3] = ti

    for key, value in components.items():
        print("****************************************************")
        print(key + ": ")
        print("Ops:", " => ".join([ "{}({}ms)".format(op, ti) for op, ti in zip(value[0], value[1])]))
        print("Total Breakdown:", value[2])
        print("Total Time:", value[3])
        print("****************************************************")
            