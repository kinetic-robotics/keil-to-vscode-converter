@net use X: "\\Mac\Home" /persistent:yes
@cd /d %1\..
%1
@net use X: /delete