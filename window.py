import pytermgui as ptg
import os
from threading import Thread

list_packages = []

def list_packagesF():
    global list_packages
    os.system("pacman -Qe > packages.txt")
    with open("packages.txt", 'r') as file:
        list_packages = [line for line in file]
    os.system('rm packages.txt')

def delete(value):
    os.system(f'sudo pacman -Rscun {value} & Y && exit 0')

def install(value):
    os.system(f'sudo pacman -S {value} & Y && exit 0')

class windowMenu():
    def __init__(self):

        # - initialization of window
        self.window = ptg.Window()

        list_package = Thread(target=list_packagesF)
        list_package.start()
        list_package.join()

        self.title = "[@#dec14e black bold] Package Manager"
        ## Displaying all packages ################################
        # 
        self.window.__add__("")
        self.window.__add__(ptg.Label("[@white black bold] Packages ", parent_align=0))
        self.containerPackages = ptg.Container() # a place to store packages
        self.containerPackages.set_style('border', '[#dec14e]{item}')
        self.containerPackages.set_style('corner', '[#dec14e]{item}')
        self.containerPackages.set_char("corner", ['╭─','─╮', '─╯', '╰─'])
        self.containerPackages.height = 15
        self.containerPackages.overflow = ptg.Overflow.SCROLL

        count = 1 # - start of count
        for package in list_packages:
            self.containerPackages.__add__(ptg.Label(f'[@white black bold] {count} ' + "[@0] " + f'[white bold] {package}', parent_align=0)) # parent_align -- 1-(Center) 2-(Right) 3-(Left)
            count += 1
        # 
        ######################################################################

        ## Buttons ###########################################################
        # 
        self.install_btn = ptg.Button("Install", onclick=self.InstallPackage)
        self.install_btn.set_style("label",'[@#32ba52 white]    {item}    ')
        self.install_btn.set_style("highlight",'[@#45ff70 white bold]    {item}    ')
        self.install_btn.on_release(self.install_btn)

        self.delete_btn = ptg.Button("Delete", onclick=self.DeletePackage)
        self.delete_btn.set_style("label",'[@#c23232 white]    {item}    ')
        self.delete_btn.set_style("highlight",'[@#ff4545 white bold]    {item}    ')
        self.delete_btn.on_release(self.delete_btn)

        self.update_btn = ptg.Button("Update", onclick=self.UpdateList)
        self.update_btn.set_style("label",'[@gray white]     {item}     ')
        self.update_btn.set_style("highlight",'[@black white bold]   {item}   ')
        self.update_btn.on_release(self.update_btn)

        self.exit_btn = ptg.Button("Exit", onclick=self.ExitFromProgram)
        self.exit_btn.set_style("label",'[@gray white]     {item}     ')
        self.exit_btn.set_style("highlight",'[@black white bold]    {item}    ')
        self.exit_btn.on_release(self.exit_btn)

        self.field_Write_Name_Package = ptg.InputField(prompt="Name package: ")
        self.field_Write_Name_Package.set_style("prompt", "[white bold]{item}")
        self.field_Write_Name_Package.set_style("value", "[white]{item}")
        # 
        ######################################################################

        ## Window properties #################################################
        # 
        # menu _______________________________________________________________
        self.window.__add__(self.containerPackages) 
        self.window.__add__("")
        self.window.__add__(self.field_Write_Name_Package)
        self.window.__add__("")
        self.window.__add__((self.install_btn, self.delete_btn))
        self.window.__add__("")
        self.window.__add__((self.update_btn, self.exit_btn))

        # properties _________________________________________________________

        self.window.center(0)
        self.window.is_dirty = True
        self.window.set_title(self.title)
        self.window.width = 70
        self.window.height = 26
        self.window.min_width = 70
        # 
        ######################################################################

    ## Functions #########################################################
    # 
    # - finish the manager's work, exit the program
    def ExitFromProgram(self, _):
        manager.stop()

    def UpdateList(self, _):
        list_package = Thread(target=list_packagesF)
        list_package.start()
        list_package.join()
        count = 1 # - start of count
        self.containerPackages = ptg.Container() # a place to store packages
        self.containerPackages.set_style('border', '[#dec14e]{item}')
        self.containerPackages.set_style('corner', '[#dec14e]{item}')
        self.containerPackages.set_char("corner", ['╭─','─╮', '─╯', '╰─'])
        self.containerPackages.height = 15
        self.containerPackages.overflow = ptg.Overflow.SCROLL
        count = 1 # - start of count
        for package in list_packages:
            self.containerPackages.__add__(ptg.Label(f'[@white black bold] {count} ' + "[@0] " + f'[white bold] {package}', parent_align=0)) # parent_align -- 1-(Center) 2-(Right) 3-(Left)
            count += 1

    def InstallPackage(self, _):
        if self.field_Write_Name_Package.value:
            value = self.field_Write_Name_Package.value
            d = Thread(target=install, args=[value])
            d.start()
            d.join()

    def DeletePackage(self, _):
        if self.field_Write_Name_Package.value:
            value = self.field_Write_Name_Package.value
            d = Thread(target=delete, args=[value])
            d.start()
            d.join()
            
    # 
    ######################################################################

## Start window ######################################################
#
with ptg.WindowManager() as manager:
    manager.add(windowMenu().window)
# 
######################################################################