"""
================
Target types def 
================

:Authors: - Florian Dupeyron <florian.dupeyron@mugcat.fr>
:Date: July 2023

original source code from  September 2018
"""

from dataclasses import dataclass, field
import re
from typing import Set, Optional, Dict, Callable

from .rule import Rule

import logging

log = logging.getLogger("target")

@dataclass(eq=True, frozen=True)
class Target:
    name: str
    rule: Rule
    deps: Set["Target"] = field(default_factory=set)
    vars: Optional[Dict[str, any]] = field(default_factory=dict)

    gen_name: Optional[Callable[[str], str]] = lambda x: x

    def __str__(self):
        return self.name

#def obj( src ):
#    """
#    Generates obj file from source src
#    """
#    log.info(f"Adding object target for {src}")
#
#    return Target(
#        name     = str(src) + ".o",
#        rule     = "cc",
#        deps     = [ src ],
#        gen_name = lambda x : "$dir_obj/" + x,
#        vars     = { "cflags" : "$cflags -D__FILENAME__=\\\"{}\\\"".format(str(src)) }
#    )
#
#def executable( name, **args ):
#    """
#    Generates executable file <name> from :
#       * srcs : source names (generate objs targets)
#       * objs : additional objs
#    """
#
#    log.info( f"Adding executable {name}" )
#    objs = []
#    for src in args.get("srcs"):
#        dd = obj( src )
#        for path in args.get( "incdirs", [] ):
#            dd.vars[ "cflags" ] += " -I" + path
#        objs.append( dd )
#
#
#    return Target(
#        name      = name,
#        rule      = "ld",
#        deps      = objs + args.get("objs", []),
#        gen_name  = lambda x : "$dir_bin/" + x,
#    )
#
#def lib( name, **args ):
#    """
#    Generates static library <name> with :
#        * srcs : source file names
#        * objs : additional objects
#    """
#    log.info(f"Adding static library {name}")
#
#    objs = []
#    for src in args.get("srcs"):
#        dd = obj( src )
#        for path in args.get( "incdirs", [] ):
#            dd.vars[ "cflags" ] += " -I" + path
#        objs.append( dd )
#    return Target(
#        name     = name + ".a",
#        rule     = "lib",
#        deps     = objs + args.get("objs", []),
#        gen_name = lambda x : "$dir_lib/" + x,
#    )
#
#def re2c( name, **args ):
#    print( "\nAdding re2c file " + str(name) )
#    mt = re.match( "(.*?).re.c", name )
#    if not mt : raise RuntimeError( "Could not match .re.c extension for target name " + repr(name) )
#    cname = mt.group(1) + ".c"
#
#    return Target(
#        name = cname,
#        rule = "re2c",
#        deps = [ name ],
#        aliases = args.get( "aliases", [] )
#    )
#