#!/usr/bin/env python3.6


# 
# Tool to easily check a kernel config file against a set of best known settings
#
#
#
# See also https://kernsec.org/wiki/index.php/Kernel_Self_Protection_Project/Recommended_Settings
#

import sys
import re

must_be_set = dict()
must_be_set_or_module = dict()
must_be_unset = dict()


def usage() -> None:
    print("Usage:")
    print("\tkernel-config-checker.py <configfile>")
    exit(0)
    
    
def process_single_line(line : str) -> None:
    global must_be_set
    global must_be_unset
    line = line.strip()
    
    match = re.search("^# (CONFIG_.*) is not set", line)
    if match:
          notset = match.group(1)
          
          if notset in must_be_set:
               print(notset, "is not set but is required to be set to y (" + must_be_set[notset] +")")

          if notset in must_be_set_or_module:
               print(notset, "is not set but is required to be set to y or m (" + must_be_set_or_module[notset] +")")
               

    match = re.search("^(CONFIG_.*)=y", line)
    if match:
          notset = match.group(1)
          
          if notset in must_be_unset:
               print(notset, "is set but is required to be not set (" + must_be_unset[notset] +")")

               

    match = re.search("^(CONFIG_.*)=m", line)
    if match:
          notset = match.group(1)
          
          if notset in must_be_set:
               print(notset, "is set as =m  but is required to be set to y (" + must_be_set[notset] +")")

          if notset in must_be_unset:
               print(notset, "is set as =m but is required to be not set (" + must_be_unset[notset] +")")
               
    


def init_arrays() -> None:
    global must_be_set
    global must_be_unset
    must_be_set["CONFIG_RANDOMIZE_BASE"] = "KASLR is required as a basic security hardening"    
    must_be_set["CONFIG_RANDOMIZE_MEMORY"] = "KASLR is required as a basic security hardening"    
    must_be_set["CONFIG_STRICT_KERNEL_RWX"] = "NX is important for buffer overflow exploit hardening"
    must_be_set["CONFIG_CC_STACKPROTECTOR"] = "Stack Protector is for buffer overflow detection and hardening"

    must_be_unset["CONFIG_DEVMEM"] = "/dev/mem is dangerous and has no legitimate users anymore"
    must_be_set["CONFIG_STRICT_DEVMEM"] = "/dev/mem is dangerous and access must be strictly limited"
    must_be_set["CONFIG_IO_STRICT_DEVMEM"] = "/dev/mem is dangerous and access must be strictly limited"
    
    must_be_set["CONFIG_DEBUG_CREDENTIALS"] = "Needed to protect against targeted corruption by rootkits"
    must_be_set["CONFIG_DEBUG_NOTIFIERS"] = "Needed to protect against targeted corruption by rootkits"
    must_be_set["CONFIG_DEBUG_LIST"] = "Needed to protect against targeted corruption by rootkits"
    must_be_set["CONFIG_DEBUG_SG"] = "Needed to protect against targeted corruption by rootkits"
    must_be_set["CONFIG_SCHED_STACK_END_CHECK"] = "Needed to protect against targeted corruption by rootkits"
    

    must_be_set["CONFIG_SECCOMP"] = "Seccomp is a security feature needed by systemd"
    must_be_set["CONFIG_SECCOMP_FILTER"] = "Seccomp is a security feature needed by systemd"
    
    must_be_set["CONFIG_HARDENED_USERCOPY"] = "Protect against ioctl buffer overflows"
    must_be_unset["CONFIG_HARDENED_USERCOPY_FALLBACK"] = "Protect against ioctl buffer overflows"
    
    must_be_set["CONFIG_SLAB_FREELIST_RANDOM"] = "Harden the slab free list with randomization"
    must_be_set["CONFIG_SLAB_FREELIST_HARDENED"] = "Harden the slab free list with randomization"
    
    must_be_set["CONFIG_VMAP_STACK"] = "Guard pages for kernel stacks"
    
    must_be_set["CONFIG_REFCOUNT_FULL"] = "Perform extensive checks on reference counting"
    must_be_set["CONFIG_FORTIFY_SOURCE"]= "Check for memory copies that might overflow a structure in str*() and mem*() functions both at build-time and run-time."    
    must_be_unset["CONFIG_ACPI_CUSTOM_METHOD"] = "Dangerous; enabling this allows direct physical memory writing"
    must_be_unset["CONFIG_COMPAT_BRK"] = "Dangerous; enabling this disables brk ASLR"
    must_be_unset["CONFIG_DEVKMEM"] = "Dangerous; enabling this allows direct kernel memory writing."
    must_be_unset["CONFIG_PROC_KCORE"] = "Dangerous; exposes kernel text image layout"
    must_be_unset["CONFIG_COMPAT_VDSO"] = "Dangerous; enabling this disables VDSO ASLR"
    must_be_unset["CONFIG_INET_DIAG"] = "Prior to v4.1, assists heap memory attacks; best to keep interface disabled"
    must_be_unset["CONFIG_LEGACY_PTYS"] = "Use the modern PTY interface (devpts) only"
    must_be_set["CONFIG_DEBUG_SET_MODULE_RONX"] = "Ensure modules have NX enabled"
    must_be_set["CONFIG_STRICT_MODULE_RWX"] = "Ensure modules have NX enabled"
    must_be_set["CONFIG_MODULE_SIG"] = "Signing of kernel modules is required"
    must_be_set["CONFIG_MODULE_SIG_FORCE"] = "Enforce module signing"
    must_be_set["CONFIG_MODULE_SIG_SHA512"] = "Use SHA512 for kernel module signing"
    
    must_be_set["CONFIG_LEGACY_VSYSCALL_NONE"] = "Modern libc no longer needs a fixed-position mapping in userspace, remove it as a possible target."
    must_be_set["CONFIG_PAGE_TABLE_ISOLATION"] = "Enable Kernel Page Table Isolation to remove an entire class of cache timing side-channels."
    must_be_unset["CONFIG_X86_X32"] = "X32 is rarely used and provides only attack surface"
    must_be_unset["CONFIG_MODIFY_LDT_SYSCALL"] = "Unused dangerous option"
    
    
def main() -> None:
    if len(sys.argv) != 2:
        usage()
        
    init_arrays()
        
    with open (sys.argv[1], "r") as myfile:
         lines = myfile.readlines()
         
    for line in lines:
        process_single_line(line)
        

if __name__ == '__main__':
    main()

