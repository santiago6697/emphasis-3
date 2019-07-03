import sys

sum = 0
cnt = 0
err_cnt = 0

for line in sys.stdin:
    try:
        data = line.strip()
        sum += float(data)
        cnt += 1
    except:
        err_cnt += 1

avg = sum/cnt

print("RTT: " + str(avg))
print("Sent packets " + str(cnt + err_cnt))
print("Retrieved packets: " + str(cnt))
print("Packets w/errors: " + str(err_cnt))
print("Mean BW: " + str(544/((avg/2))) + " kbps")
