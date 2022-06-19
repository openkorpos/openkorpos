#!/usr/bin/env python3
# Refer to license.txt for license information.

import click
import json
import os


class NinjaTemplate:
    BASE = '''
root = data
builddir = build
cc = grep '"flagged":false'
ccd = cat
ld = cat

rule compile
    description = "Collecting corpus fragments"
    command = $cc $in > $out

rule compile_debug
    description = "Collecting corpus fragments"
    command = $ccd $in > $out

rule link
    description = "Amalgamating corpus"
    command = $ld $in > $out

'''

    FRAGMENT = 'build $builddir/%(fragment) : %(compile) $root/%(fragment)'
    LINK_FIRST = 'build $builddir/%(target).jsonl: link $'
    LINK_FRAGMENT = '    $builddir/%(fragment) $'


def load_rule(rule: str):
    with open(os.path.join(os.path.split(__file__)[0], 'rules', f'{rule}.json'), 'r') as rule_file:
        rule = json.load(rule_file)

    return rule


def rules_to_ninja(rules: list, flagged: bool = False):
    build = {}

    for rule in rules:
        for k in rule['sources'].keys():
            if k not in build.keys():
                build[k] = []

            for fragment in rule['sources'][k]:
                build[k].append(fragment)

    out = NinjaTemplate.BASE

    for target, fragments in build.items():
        for fragment in fragments:
            out += NinjaTemplate.FRAGMENT.replace('%(fragment)', fragment) \
                                         .replace('%(compile)', 'compile_debug' if flagged else 'compile')
            out += "\n"
        
        out += NinjaTemplate.LINK_FIRST.replace('%(target)', target)
        out += "\n"
        
        for fragment in fragments:
            out += NinjaTemplate.LINK_FRAGMENT.replace('%(fragment)', fragment)
            out += "\n"

        out += "\n\n"

    return out


@click.group()
def cli():
    pass


@cli.command()  # @cli, not @click!
@click.argument('rules', nargs=-1)
@click.option('--flagged/--no-flagged', default=False, help='Add flagged sentences to corpus. (Default off)')
def ningen(rules, flagged):
    '''Generate ninja build rules'''
    parsed_rules = []

    for rule in rules:
        print(f'Processing rule: {rule}')
        parsed_rules.append(load_rule(rule))

    build_out = rules_to_ninja(parsed_rules, flagged)
    
    with open('build.ninja', 'w') as ninja_file:
        ninja_file.write(build_out)
        print('Now run ninja!')


if __name__ == '__main__':
    cli()