import matplotlib.pyplot as plt
import numpy as np

#x = np.arange(0, 20, 0.2)
#y = [x for x in range(100)]
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot([x for x in range(15)], [y for y in range(15)], 'ro')
#ax.axis([0, 6, 0, 20])
plt.xlabel('time (s)')
plt.ylabel('messages received')
plt.title('Network Performance Analysis')
plt.grid(True)
plt.savefig("test.png")
plt.show()
