#NoTrayIcon
HotKeySet("!#+1", "func1")
HotKeySet("!#+2", "func2")
HotKeySet("!#+3", "func3")
HotKeySet("!#+4", "func4")
HotKeySet("!#+5", "func5")
HotKeySet("!#+q", "quit")
While 1
	Sleep(15)
wend

Func func1()
run("recmon.exe 1","")
endfunc

Func func2()
run("recmon.exe 2","")
endfunc

Func func3()
run("recmon.exe 3","")
endfunc

Func func4()
run("recmon.exe 4","")
endfunc

Func func5()
run("recmon.exe 5","")
endfunc

Func quit()
Exit
endfunc