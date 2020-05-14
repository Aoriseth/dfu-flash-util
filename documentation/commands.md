List connected devices:  
`dfu-util -l`

Backup device firmware:  
`dfu-util -a <device-alt> -U <filename> -s <memory-address>:<bytes>`

Flash device firmware:  
`dfu-util -a <device-alt> -s <memory-address>:leave -D <filename>`
