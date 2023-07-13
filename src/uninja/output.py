"""
######################
# Output ninja rules #
######################

  Florian Dupeyron (floolfy)
  September 2018

"""

from .target import Target
from .rule   import Phony

def add_deps( ss, ruleset, dep ):
    """
    Adds dependency rule to dict ss. Value is a tuple containing
    a list of dependency file names, and the proper target rule.
    If dep is a string, no rule is added. is actually a postfix
    tree walk.
    """
    if isinstance( dep, Target ):
        if ( dep.name in ss ) and not ( dep is ss[dep.name][0] ):
            print( repr(dep) )
            print( repr(ss[dep.name] ) )
            raise RuntimeError( "Duplicate entry : " + dep.name )

        # Add rule in ruleset (only if needed)
        ruleset.add(dep.rule)


        #########################################
        # TODO # More explicit var names

        depnames = ""
        for ch in dep.deps :
            depnames += str(ch) + " "
            add_deps( ss, ruleset, ch )

        ss[ dep.name ] = (dep, depnames)

def build_file( fhandle, target_list ):
    if not isinstance( target_list, list ):
        raise TypeError("Must be list of targets")

    # Step 1 # Constructing set of targets
    ss      = dict()
    ruleset = set()
    for tt in target_list : add_deps( ss, ruleset, tt )

    # Step 2 # Print rules
    for rule in ruleset:
        # The phony rule is not added to the output file
        if not isinstance(rule, Phony):
            print(f"rule {rule.name}", file=fhandle)
            print(f"    command = {rule.command}", file=fhandle)
            if rule.description is not None: print(f"    description = {rule.description}", file=fhandle)
            if rule.depfile     is not None: print(f"    depfile     = {rule.depfile}"    , file=fhandle)
            print("", file=fhandle)


    # Step 3 # Printing targets
    for rr, dnames in ss.values():
        print( "build {name} : {rule} {deps}".format( name = rr.gen_name(rr), rule = rr.rule, deps = dnames),file=fhandle)
        for k, v in rr.vars.items():
            print( "    {} = {}".format(k,v), file=fhandle)
        print("",file=fhandle)
