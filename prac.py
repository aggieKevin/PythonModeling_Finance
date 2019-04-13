def insertionSort1(n,arr):
    l=len(arr)
    last=arr[-1]
    found=False
    for i in range(l-2,-1,-1):
        if arr[i]>last:
                arr[i+1]=arr[i]               
        else:
            found=True
            arr[i+1]=last
        print(*arr)
        if found==True:
            break
    arr[0]=last
    print(*arr)

def insertionSort2(n,arr):
    for l in range(1,len(arr)):
        for compare in range(0,l):
            if arr[l]<arr[compare]:
                # insert arr[l] before arr[compare]
                arr[compare],arr[compare+1:l+1]=arr[l],arr[compare:l]
    return arr
                
        
arr=[int(i) for i in '2 3 4 5 6 7 8 9 10 1'.split()]  
insertionSort1(n, arr)

x[3],x[4:6]=x[5],x[3:5]