
game_config ={}
game_config['partial_resist_multiplier'] = 0.94 #lvl+3
game_config['chance_to_miss'] = 0.17 #lvl+3
game_config['base_mana'] = 1961
game_config['base_crit'] = 0.0091
def make_talents():
    talents = {}
    talents['elemental_precision'] =	0
    talents['improved_frostbolt'] = 	0
    talents['ice_shards'] =	0
    talents['piercing_ice']=	0
    talents['frost_channeling']=	0
    talents['empowered_frostbolt']=	0
    talents['summon_water_elemental']=	0
    talents['winters_chill']=	0
    talents['arctic_winds']=	0
    talents['icy_veins']=	0
    talents['cold_snap']=	0
    #Fire Talents
    talents['improved_fireball']=	0
    talents['ignite'] =	0
    talents['incinerate']=	0
    talents['master_of_elements']=	0
    talents['critical_mass'] =	0
    talents['playing_with_fire']=	0
    talents['fire_power']=	0
    talents['pyromaniac']=	0
    talents['molten_fury']=	0
    talents['empowered_fireball']=	0
    talents['improved_scorch']=	0
    talents['combustion']=	0
    talents['pyroblast']=	0
    #Arcane Talents
    talents['arcane_focus']=	0
    talents['arcane_impact']=	0
    talents['arcane_concentration']=	0
    talents['arcane_meditation']=	0
    talents['arcane_mind']=	0
    talents['arcane_potency']=	0
    talents['arcane_instability']=	0
    talents['empowered_arcane_missiles']=	0
    talents['arcane_power']=	0
    talents['spell_power']=	0
    talents['mind_mastery']=	0
    talents['prescence_of_mind']=	0
    # misc
    # force clearcasting. If 1, allways set clearcasting, if -1 allways disable clearcasting
    talents['force_clearcasting'] =	0
    talents['improved_scorch_on_target'] = 0
    return talents

def make_fire_talents():
    talents = make_talents()
    #Frost Talents
    talents['elemental_precision'] =	3
    talents['ice_shards'] =	2
    talents['icy_veins']=	1
    #Fire Talents
    talents['improved_fireball']=	5
    talents['ignite'] =	5
    talents['incinerate']=	2
    talents['master_of_elements']=	3
    talents['critical_mass'] =	3
    talents['playing_with_fire']=	3
    talents['fire_power']=	5
    talents['pyromaniac']=	3
    talents['molten_fury']=	2
    talents['empowered_fireball']=	5
    talents['improved_scorch']=	3
    talents['combustion']=	1

    return talents
def make_arcane_fire_talents():
    talents = make_talents()
    #Arcane Talents
    talents['arcane_focus']=	5
    talents['arcane_impact']=	3
    talents['arcane_concentration']=	5
    talents['arcane_meditation']=	3
    talents['arcane_mind']=	5
    talents['arcane_potency']=	3
    talents['arcane_instability']=	3
    talents['empowered_arcane_missiles']=	3
    talents['arcane_power']=	1
    talents['spell_power']=	2
    talents['mind_mastery']=	5
    talents['prescence_of_mind']=	1
    #Frost Talents
    talents['elemental_precision'] =	3
    #Fire Talents
    talents['improved_fireball']=	5
    talents['ignite'] =	5
    talents['incinerate']=	2
    talents['pyroblast'] =	1
    return talents
def make_arcane_frost_talents():
    # https://legacy-wow.com/tbc-talents/mage-talents/?tal=2520050300030150333125000000000000000000000000535000310010000000000
    talents = make_talents()
    #Arcane Talents
    talents['arcane_focus']=	5
    talents['arcane_impact']=	3
    talents['arcane_concentration']=	5
    talents['arcane_meditation']=	3
    talents['arcane_mind']=	5
    talents['arcane_potency']=	3
    talents['arcane_instability']=	3
    talents['empowered_arcane_missiles']=	3
    talents['arcane_power']=	1
    talents['spell_power']=	2
    talents['mind_mastery']=	5
    talents['prescence_of_mind']=	1
    #Frost Talents
    talents['elemental_precision'] =	3
    talents['improved_frostbolt'] = 	5
    talents['ice_shards'] =	5
    talents['piercing_ice']=	3
    talents['icy_veins']=	1
    talents['frost_channeling']=	1
    return talents
def make_frost_talents():
    talents = {}
    #Frost Talents
    talents['elemental_precision'] =	3
    talents['improved_frostbolt'] = 	5
    talents['ice_shards'] =	5
    talents['piercing_ice']=	3
    talents['icy_veins']=	1
    talents['frost_channeling']=	3
    talents['empowered_frostbolt']=	5
    talents['summon_water_elemental']=	1
    talents['winters_chill']=	5
    talents['arctic_winds']=	5
    talents['cold_snap']=	1
    return talents

class Spell:
    def __init__(self,damage, mana, cast_time, spellpower_coefficient,
                cooldown = 0,
                crit_multiplier=0.5,
                crit_chance_talent_modifier = 0,
                other = None,
                dot=0,
                dot_spellpower_coefficient=0,
                school = None
                ):
        self.damage = float(damage)
        self.mana = float(mana)
        self.cast_time = float(cast_time)
        self.spellpower_coefficient = float(spellpower_coefficient)
        self.cooldown = float(cooldown)
        self.other = other
        self.crit_multiplier = float(crit_multiplier)
        self.crit_chance_talent_modifier = float(crit_chance_talent_modifier)
        self.dot = float(dot)
        self.dot_spellpower_coefficient = float(dot_spellpower_coefficient)
        self.school=school
        self.damage_mul_talents = 1
        return

    def update_damage(self,game_config, stats):
        #print(stats['actual_spellpower'][self.school])
        #self.average_damage = self.actual_damage
        '''if 'arcane_blast_1_0speed_0mana' == self.name:
            print(self.name, f'dmg { self.damage:.2f}, +spelldamage { self.spellpower_coefficient:.2f} * {stats["actual_spellpower"][self.school]:.2f} = { self.spellpower_coefficient*stats["actual_spellpower"][self.school]:.2f} ')'''
        self.actual_damage = self.damage
        self.actual_damage+= self.spellpower_coefficient*stats['actual_spellpower'][self.school]
        self.actual_damage *= self.damage_mul_talents
        crit_chance = np.min([(stats['crit_chance']+self.crit_chance_talent_modifier), 0.99] )
        #print([(stats['crit_chance']+self.crit_chance_talent_modifier), stats['actual_hit'][self.school]] )
        #print(crit_chance, stats['crit_chance'],self.crit_chance_talent_modifier, self.school)
        crit_bonus = self.actual_damage*self.crit_multiplier*crit_chance
        if hasattr(self, 'ignite_bonus'):
            # if spell has ignite, you may get to chain it, calculate up to 3
            # ignite_bonus = the damage multipleier from ignite
            if not 'no_roll' in self.name:
                crit_bonus += 0.5*self.ignite_bonus*self.actual_damage*crit_chance**2*stats['actual_hit'][self.school]
                if not 'one_roll' in self.name:
                    crit_bonus += 0.5*self.ignite_bonus*self.actual_damage*crit_chance**3*stats['actual_hit'][self.school]**2
        '''if 'arcane_blast_1_0speed_0mana' == self.name:
            print(self.name, f'dmg { self.actual_damage:.2f}, crit { crit_chance:.3f} * {self.actual_damage*self.crit_multiplier:.2f} = { crit_bonus:.2f}')'''
        # apparently it is a two-roll system
        #crit_bonus = crit_bonus/(stats['actual_hit'][self.school]) # this is a one-roll system, a crit is guaranteed to hitif 'arcane_blast_1_0speed_0mana' == self.name:
        self.average_damage = self.actual_damage + crit_bonus
        dot = self.dot+self.dot_spellpower_coefficient*stats['actual_spellpower'][self.school]
        self.average_damage+=dot*self.damage_mul_talents
        self.average_damage*=game_config['partial_resist_multiplier']
        self.average_damage*=stats['actual_hit'][self.school]
        '''if 'arcane_blast_1_0speed_0mana' == self.name:
            print(self.name, f'dmg { self.average_damage:.2f}, dps { self.average_damage/1.51:.3f}')'''

        return

def make_spell_list():
    spells = {}
    # two possible extra ignite tick
    spells['fireball_13_one_tick'] = Spell(719.5, 425, 3.5, 1, dot= 21, school='fire')
    spells['fireball_13_two_tick'] = Spell(719.5, 425, 3.5, 1, dot= 42, school='fire')
    spells['fireball_13_three_tick'] = Spell(719.5, 425, 3.5, 1, dot= 63, school='fire')
    spells['fireball_13_four_tick'] = Spell(719.5, 425, 3.5, 1, dot= 84, school='fire') #84 damage over 12 sec
    # only possible one extra ignite tick
    spells['fireball_13_one_tick_one_roll'] = Spell(719.5, 425, 3.5, 1, dot= 21, school='fire')
    spells['fireball_13_two_tick_one_roll'] = Spell(719.5, 425, 3.5, 1, dot= 42, school='fire')
    spells['fireball_13_three_tick_one_roll'] = Spell(719.5, 425, 3.5, 1, dot= 63, school='fire')
    spells['fireball_13_four_tick_one_roll'] = Spell(719.5, 425, 3.5, 1, dot= 84, school='fire') #84 damage over 12 sec
    # no possible extra ignite tick
    spells['fireball_13_one_tick_no_roll'] = Spell(719.5, 425, 3.5, 1, dot= 21, school='fire')
    spells['fireball_13_two_tick_no_roll'] = Spell(719.5, 425, 3.5, 1, dot= 42, school='fire')
    spells['fireball_13_three_tick_no_roll'] = Spell(719.5, 425, 3.5, 1, dot= 63, school='fire')
    spells['fireball_13_four_tick_no_roll'] = Spell(719.5, 425, 3.5, 1, dot= 84, school='fire') #84 damage over 12 sec


    spells['scorch_9'] = Spell(333, 180, 1.5, 1.5/3.5, school='fire')
    spells['scorch_9_one_roll'] = Spell(333, 180, 1.5, 1.5/3.5, school='fire')
    spells['scorch_9_no_roll'] = Spell(333, 180, 1.5, 1.5/3.5, school='fire')

    spells['fireblast'] = Spell(725,465,1.5, 1.5/3.5, school='fire')
    spells['pyroblast'] = Spell(960,460,6,1.15, dot= 312, dot_spellpower_coefficient = 0.2, school='fire') # damage +dot
    spells['pom_pyroblast'] = Spell(960,460,6,1.15,cooldown=180, dot= 312, dot_spellpower_coefficient = 0.2, school='fire') # damage +dot
    spells['pom_pyroblast_one_roll'] = Spell(960,460,6,1.15,cooldown=180, dot= 312, dot_spellpower_coefficient = 0.2, school='fire') # damage +dot
    spells['pom_pyroblast_no_roll'] = Spell(960,460,6,1.15,cooldown=180, dot= 312, dot_spellpower_coefficient = 0.2, school='fire') # damage +dot

    spells['arcane_missiles_10'] = Spell(1300, 740, 5, 5/3.5, school='arcane')
    spells['arcane_blast_1_0speed_0mana'] = Spell(720, 195, 2.5, 2.5/3.5, school='arcane')
    #Arcane Blast ramp-up speed:	0.3
    #Arcane Blast ramp-up mana:	0.75
    spells['arcane_blast_1_1speed_1mana'] = Spell(720, 195*(1+0.75*1), 2.5-0.33*1, 2.5/3.5, school='arcane')
    spells['arcane_blast_1_2speed_2mana'] = Spell(720, 195*(1+0.75*2), 2.5-0.33*2, 2.5/3.5, school='arcane')
    spells['arcane_blast_1_3speed_3mana'] = Spell(720, 195*(1+0.75*3), 2.5-0.33*3, 2.5/3.5, school='arcane')
    spells['arcane_blast_1_1speed_0mana'] = Spell(720, 195, 2.5-0.33*1, 2.5/3.5, school='arcane')
    spells['arcane_blast_1_2speed_0mana'] = Spell(720, 195, 2.5-0.33*2, 2.5/3.5, school='arcane')
    spells['arcane_blast_1_3speed_0mana'] = Spell(720, 195, 2.5-0.33*3, 2.5/3.5, school='arcane')
    #waterbolt Waterbolt:	521.5 Waterbolt Time:	2.5
    # water_elemental_dps = 250
    # water_elemental_duration = 45
    # water_elemental_cooldown = 180
    # water_elemental_mana = 150*15*0.16 # base_int*mana_per_int*16%
    spells['frostbolt_13'] = Spell(605, 330, 3, (3.0/3.5)*0.95, school='frost')
    spells['water_elemental'] = Spell(250*45,150*15*0.16, 1.5,0, cooldown = 180 , school='frost')

    spells['evocation'] = Spell(0,0,8,0, cooldown = 8*60,school='arcane') #mana should be -60% of mana
    return spells

import copy
import numpy as np
def update_stats(old_stats,talents, game_config):
    stats = copy.deepcopy(old_stats)
    stats['actual_spellpower']={}
    stats['actual_spellpower']['fire'] = stats['common_spell_damage'] + stats['fire_damage']
    stats['actual_spellpower']['arcane'] = stats['common_spell_damage'] + stats['arcane_damage']
    stats['actual_spellpower']['frost'] = stats['common_spell_damage'] + stats['frost_damage']
    stats['actual_hit']={}
    stats['actual_hit']['fire'] = 1-game_config['chance_to_miss'] + 0.01*stats['hit_rating']/12.62
    stats['actual_hit']['arcane'] = 1-game_config['chance_to_miss'] + 0.01*stats['hit_rating']/12.62
    stats['actual_hit']['frost'] = 1-game_config['chance_to_miss'] + 0.01*stats['hit_rating']/12.62
    stats['fraction_haste'] = 0.01*stats['haste_rating'] / 15.77
    # talents
    stats['actual_hit']['fire']+= 0.01*talents['elemental_precision']
    stats['actual_hit']['frost']+= 0.01*talents['elemental_precision']
    stats['actual_hit']['arcane']+= 0.02*talents['arcane_focus']
    # max 1
    stats['actual_hit']['fire'] = min([0.99,stats['actual_hit']['fire']])
    stats['actual_hit']['frost'] = min([0.99,stats['actual_hit']['frost']])
    stats['actual_hit']['arcane'] = min([0.99,stats['actual_hit']['arcane']])

    stats['intellect'] = stats['intellect']*(1+0.03*talents['arcane_mind'])
    # MP5 = 5 * (0.001 + sqrt(Int) * Spirit * Base_Regen) from: https://www.wowhead.com/forums/topic/18199
    # see https://wowwiki-archive.fandom.com/wiki/Talk:Spirit for the Base_Regen value at lvl 70 = 0.009327
    stats['mp5_from_spirit'] = 5 * (0.001 + np.sqrt(stats['intellect']) * stats['spirit'] * 0.009327)
    stats['mp5_in_combat']=stats['mp5_from_spirit']*(0.1*talents['arcane_meditation']+0.3*talents['mage_armor']) + stats['mp5']
    #stats['mp5_from_spirit'] = stats['spirit']/4/2*5 # 4 spirit gives 1 mana every tick, a tick occurs every 2 seconds
    stats['mp5_out_of_combat'] = stats['mp5_from_spirit'] + stats['mp5']
    for school in ['fire','arcane','frost']:
        stats['actual_spellpower'][school] += 0.05*talents['mind_mastery']*stats['intellect']
        stats['actual_spellpower'][school] += 0.07*talents['spellfire_set']*stats['intellect']
    # things that depend on int
    stats['mana'] = game_config['base_mana']+stats['intellect']*15
    stats['crit_chance'] = game_config['base_crit'] + 0.01*stats['crit_rating']/22.1 +0.01*stats['intellect']/80

    return stats

def fix_spells(stats, talents, spells):
    for spell in spells:
        spells[spell].actual_mana = spells[spell].mana
        spells[spell].actual_cast_time = spells[spell].cast_time
        spells[spell].damage_mul_talents = 1
        spells[spell].name = spell
    if talents['improved_scorch']==3:
        talents['improved_scorch_on_target']=5

    # improved/empowered frostbolt
    for spell in spells:
        if 'frostbolt' in spell:
            spells[spell].actual_cast_time -= 0.1*talents['improved_frostbolt']
            spells[spell].spellpower_coefficient = (3.0/3.5)*0.95 +0.02*talents['empowered_frostbolt']
            spells[spell].crit_chance_talent_modifier = 0.01*talents['empowered_frostbolt']
    # frost spells
    for spell in spells:
        if spells[spell].school=='frost':
            spells[spell].crit_multiplier = 0.5 + 0.1*talents['ice_shards'] #ice_shards
            spells[spell].crit_multiplier +=0.125*talents['spell_power']
            spells[spell].damage_mul_talents *= (1+0.02*talents['piercing_ice']) #piercing_ice
            spells[spell].actual_mana -= 0.05*talents['frost_channeling']*spells[spell].mana
            spells[spell].damage_mul_talents *= (1+0.01*talents['arctic_winds']) #piercing_ice
            spells[spell].crit_chance_talent_modifier += 0.02*talents['winters_chill']

    # improved fireball
    for spell in spells:
        if 'fireball' in spell:
            spells[spell].actual_cast_time -= 0.1*talents['improved_fireball']
            spells[spell].spellpower_coefficient = 1.0 +0.03*talents['empowered_fireball']

    for spell in spells:
        if 'scorch' in spell or 'fireblast' in spell:
            spells[spell].crit_chance_talent_modifier = 0.02*talents['incinerate']
    for spell in spells:
        if spells[spell].school=='fire':
            spells[spell].crit_multiplier = 0.5+0.125*talents['spell_power']
            ignite_bonus =  (1+spells[spell].crit_multiplier)*0.08*talents['ignite'] # the damage multipleier from ignite
            spells[spell].ignite_bonus = ignite_bonus
            spells[spell].crit_multiplier += ignite_bonus
            spells[spell].crit_chance_talent_modifier += 0.02*talents['critical_mass']
            spells[spell].damage_mul_talents *= (1+0.02*talents['fire_power']) #fire_power
            spells[spell].actual_mana -= spells[spell].mana*0.01*talents['pyromaniac']
            spells[spell].crit_chance_talent_modifier += 0.01*talents['pyromaniac']
            spells[spell].damage_mul_talents *= (1+0.03*talents['improved_scorch_on_target'])

    for spell in spells:
        if spells[spell].school=='arcane':
            spells[spell].crit_multiplier =0.5+0.125*talents['spell_power']
            if talents['curse_of_shadow']: # +10% more damage from arcane
                if talents['malediction']: # +3% more damage from curse of elements/shadow
                    spells[spell].damage_mul_talents *= 1.13
                else:
                    spells[spell].damage_mul_talents *= 1.1
            if talents['misery']: # +5% damage
                    spells[spell].damage_mul_talents *= 1.05
    for spell in spells:
        if 'arcane_blast' in spell:
            spells[spell].crit_chance_talent_modifier += 0.02*talents['arcane_impact']
            if talents['2_tier5_set_bonus']:
                spells[spell].actual_mana += 0.2 * 195 # this acts only on bae mana, not on the added mana from the debuff stack
                spells[spell].damage_mul_talents *= 1.2
            #print(spells[spell].damage_mul_talents)
    for spell in spells:
        if 'arcane_missiles' in spell:
            spells[spell].spellpower_coefficient = 5/3.5+0.15*talents['empowered_arcane_missiles']
            spells[spell].actual_mana += spells[spell].mana*0.02*talents['empowered_arcane_missiles']


    # frost and fire stuff
    for spell in spells:
        if spells[spell].school=='frost' or spells[spell].school=='fire':
            spells[spell].actual_mana -= 0.01*talents['elemental_precision']*spells[spell].mana
            if talents['curse_of_elements']: # +10% more damage from fire/frost
                if talents['malediction']: # +3% more damage from curse of elements/shadow
                    spells[spell].damage_mul_talents *= 1.13
                else:
                    spells[spell].damage_mul_talents *= 1.1
            if talents['misery']: # +5% damage
                    spells[spell].damage_mul_talents *= 1.05

    # all spells
    for spell in spells:
        spells[spell].damage_mul_talents *= 1+0.01*talents['playing_with_fire']
        spells[spell].damage_mul_talents *= 1+0.2*0.1*talents['molten_fury']
        if talents['force_clearcasting']==0:
            spells[spell].actual_mana *= (1-0.02*talents['arcane_concentration'])
            spells[spell].crit_chance_talent_modifier += 0.01*talents['arcane_potency']
        elif talents['force_clearcasting']==1:
            spells[spell].actual_mana *= (1-0.2*talents['arcane_concentration'])
            spells[spell].crit_chance_talent_modifier += 0.1*talents['arcane_potency']
        else: # talents['force_clearcasting']==-1:
            spells[spell].actual_mana *= 1
            spells[spell].crit_chance_talent_modifier += 0
        spells[spell].crit_chance_talent_modifier += 0.01*talents['arcane_instability']
        spells[spell].damage_mul_talents *= 1+0.01*talents['arcane_instability']
        if talents['judgement_of_wisdom']:
            spells[spell].actual_mana -= 74 *0.5 * stats['actual_hit'][spells[spell].school] # 50% chance to return 74 mana
            if 'arcane_missiles' in spell: # arcane missiles hits 5 times
                spells[spell].actual_mana -= 4*74 *0.5 * stats['actual_hit'][spells[spell].school] # 50% chance to return 74 mana
        #print(spells[spell].damage_mul_talents, spells[spell].school)
    for spell in spells:
        if spells[spell].school=='frost' or spells[spell].school=='fire':
            crit_chance = np.min([(stats['crit_chance']+spells[spell].crit_chance_talent_modifier), 0.99] )
            spells[spell].actual_mana -= spells[spell].mana*0.1*talents['master_of_elements']*crit_chance #ice_shards



# icy veins and water elemental not addressed
# combustion and improved scorch not addressed
# clearcasting averaged

def get_spells_stats(stats, talents, game_config):
    spells = make_spell_list()
    new_stats = update_stats(stats,talents, game_config)
    fix_spells(new_stats, talents, spells)
    for spell in spells:
        spells[spell].update_damage(game_config,new_stats)
    return spells, new_stats

def get_dps_mps_rotation(spells):
    rot_mana = 0
    rot_damage = 0
    rot_time = 0
    for spell in spells:
        rot_mana += spell.actual_mana
        rot_damage += spell.average_damage
        rot_time += spell.actual_cast_time
    dps = rot_damage/rot_time
    mps = rot_mana/rot_time
    return dps, mps
def simulate_combustion(spell, talents, stats):
    np.random.seed(42)
    base_crit_chance = np.min([(stats['crit_chance']+spell.crit_chance_talent_modifier), 0.99] )
    crit_multiplier = 0.5+0.125*talents['spell_power']
    crit_bonus = spell.actual_damage*crit_multiplier
    one_ignite_tick_damage = 0.5*spell.ignite_bonus*spell.actual_damage
    base_mana = spell.mana*(1-0.01*talents['pyromaniac']-0.01*talents['elemental_precision'])
    crit_mana = base_mana*(1-0.1*talents['master_of_elements'])
    cycles_damage = []
    cycles_mana = []
    cycles_time = []

    cycles_to_simulate = 10000
    for cycle in range(cycles_to_simulate):
        cycle_damage = 0
        cycle_mana = 0
        cycle_time = 0
        remaining_ignite_damage = 0
        combustions_stack = 1
        crits = 0
        while remaining_ignite_damage>0 or combustions_stack>0:
            crit_chance = base_crit_chance + 0.1*combustions_stack
            r = np.random.random()
            if r < stats['actual_hit']['fire']:
                if np.random.random() < 0.02*talents['arcane_concentration']:
                    cycle_mana -= base_mana #clearcasting
                r2 = np.random.random()
                if r2 < crit_chance: #crit
                    cycle_damage += spell.actual_damage + crit_bonus
                    remaining_ignite_damage += one_ignite_tick_damage
                    cycle_damage += remaining_ignite_damage
                    cycle_mana += crit_mana
                    crits += 1
                else:
                    cycle_damage += spell.actual_damage
                    cycle_damage += remaining_ignite_damage
                    remaining_ignite_damage = 0
                    cycle_mana += base_mana
                    combustions_stack += 1
            else:
                cycle_damage += remaining_ignite_damage
                remaining_ignite_damage = 0
                cycle_mana += base_mana
            cycle_time += 3
            if crits>2:
                combustions_stack = 0
        #damage_diff = cycle_damage - spell.average_damage*cycle_time/3
        #mana_diff = cycle_mana - spell.actual_mana*cycle_time/3
        cycles_damage.append( cycle_damage*game_config['partial_resist_multiplier'])
        cycles_mana.append(cycle_mana)
        cycles_time.append(cycle_time)
    #print(cycles_damage_diff, cycles_mana_diff)
    return np.average(cycles_damage), np.average(cycles_mana), np.average(cycles_time)

def optimize_cycles_return_damage(stats, times, talents, expensive_rot, cheap_rot, return_fractions=False , IV_replace=None):
    def find_damage(casting_times, available_manas, expensive_rot, cheap_rot):
        expensive_rot_times = (available_manas - casting_times * cheap_rot[1])/(expensive_rot[1]-cheap_rot[1])
        cheap_rot_times = casting_times-expensive_rot_times
        max_rot_time = available_manas/cheap_rot[1]# max time you can do rotation

        damage = np.zeros(casting_times.shape)
        damage_burn = np.zeros(casting_times.shape)
        damage_save = np.zeros(casting_times.shape)

        damage[cheap_rot_times<0] = expensive_rot[0]*casting_times[cheap_rot_times<0]
        #print('dmg:',damage[0], casting_times[0],expensive_rot[0] )
        damage_burn[cheap_rot_times<0] = expensive_rot[0]*casting_times[cheap_rot_times<0]
        damage_save[cheap_rot_times<0] = 0

        damage[cheap_rot_times>0] = expensive_rot[0]*expensive_rot_times[cheap_rot_times>0]+cheap_rot[0]*cheap_rot_times[cheap_rot_times>0]
        damage_burn[cheap_rot_times>0] = expensive_rot[0]*expensive_rot_times[cheap_rot_times>0]
        damage_save[cheap_rot_times>0] = cheap_rot[0]*cheap_rot_times[cheap_rot_times>0]

        damage[casting_times>max_rot_time] = cheap_rot[0]*max_rot_time[casting_times>max_rot_time]
        damage_save[casting_times>max_rot_time] = cheap_rot[0]*max_rot_time[casting_times>max_rot_time]
        damage_burn[casting_times>max_rot_time] = 0


        return damage, damage_burn, damage_save
    # time
    IVtime = 0 # effective time spent in IV, save rotation might not work in this
    times_mod = copy.deepcopy(times)
    if not talents['disable_arcane_power']:
        times_mod += 0.3*15*talents['arcane_power']
    if not talents['disable_icy_veins']:
        times_mod += 0.2*20*talents['icy_veins']
        IVtime += (20+0.2*20)*talents['icy_veins']
        if not talents['disable_arcane_power']:
            times_mod += 15*0.3*0.2*talents['arcane_power']*talents['icy_veins'] # if both AP and IV
            IVtime += (0.3*15+15*0.3*0.2)*talents['arcane_power']*talents['icy_veins']
    if not talents['disable_cold_snap']:
        times_mod += 0.2*20*talents['icy_veins']*talents['cold_snap']
        IVtime += (20+0.2*20)*talents['icy_veins']*talents['cold_snap']
    #print(IVtime)
    #print(times_mod[0]-times[0])
    times_mod *= (1+stats['fraction_haste']) # multiply time available by haste instead of dividing every spell by it
    # mana
    base_manas = stats['mana']*1 + (stats['mp5_in_combat']/5)*times+0.05*talents['shadow_priest_dps']*times
    #print(stats['mana'],(stats['mp5_in_combat']/5)*times[-1],base_manas[-1])
    #print(stats['mp5_in_combat']/5)
    #print(stats['mana'])
    #print(stats['intellect'])
    #print(stats['spirit'])
    base_manas+= talents['innervate'] * 20*stats['mp5_from_spirit']/5*(4-0.1*talents['arcane_meditation']-0.3*talents['mage armor'])
    #print(20*stats['mp5_from_spirit']/5*(4-0.1*talents['arcane_meditation']+0.3*talents['mage armor']) ,'mana from innervate')
    base_manas += talents['misc_add_mana']

    # combustion

        #print(2.5*spells_forced_crit['fireball_13_one_tick'].average_damage, spells_forced_crit['fireball_13_one_tick'].actual_mana*2.5, spells_forced_crit['fireball_13_one_tick'].actual_cast_time*2.5)
        #print(2.5*spells_forced_crit['fireball_13_one_tick'].average_damage/(spells_forced_crit['fireball_13_one_tick'].actual_cast_time*2.5))
        #combustion_damage = 2.5*(spells_forced_crit['fireball_13_one_tick'].average_damage-spells_not_forced_crit['fireball_13_one_tick'].average_damage)

    add_damage = 0
    if not talents['disable_combustion']:
        if talents['combustion']:
            fire_spells, mod_stats = get_spells_stats(stats, talents, game_config)
            combustion_damage, combustion_mana, combustion_time = simulate_combustion(fire_spells['fireball_13_one_tick'], talents, mod_stats)
            #print(combustion_damage, combustion_mana, combustion_time)
            add_damage += combustion_damage
            base_manas -= combustion_mana
            times_mod -= combustion_time

    #keys: 'disable_arcane_power', 'disable_icy_veins', 'disable_cold_snap', 'disable_water_elemental', 'disable_combustion', 'disable_PoM_pyro', 'ignore_scorch_ramp'
    if not talents['ignore_scorch_ramp']:
        if talents['improved_scorch']==3:
            spells, _ = get_spells_stats(stats, talents, game_config)
            add_damage += (1+0.03*2)/1.15*spells['scorch_9'].average_damage*5
            base_manas -= spells['scorch_9'].actual_mana*5
            times_mod -= spells['scorch_9'].actual_cast_time*5
            #print(combustion_damage)
            #base_manas -= 3*spells_forced_crit['fireball_13_one_tick'].actual_mana
            #times_mod -=  3*spells_forced_crit['fireball_13_one_tick'].actual_cast_time
    if not talents['disable_PoM_pyro']:
        if talents['prescence_of_mind'] and talents['pyroblast']:
            fire_spells, mod_stats = get_spells_stats(stats, talents, game_config)
            spell = fire_spells['pom_pyroblast']
            if talents['arcane_power'] and not talents['disable_arcane_power']:
                #print(spell.average_damage*1.3)
                add_damage += spell.average_damage*1.3
                base_manas -= spell.actual_mana*1.3
            else:
                add_damage += spell.average_damage
                base_manas -= spell.actual_mana
            times_mod -= 2.5 # the casttime is 1.5, but you sacrifice 1s because you do not use POM for AB
    if not talents['disable_water_elemental']:
        if talents['summon_water_elemental']:
            frost_spells, mod_stats = get_spells_stats(stats, talents, game_config)
            spell = frost_spells['water_elemental']
            #add_damage += spell.average_damage # <- this is wrong because it assumes things about your talents

            #Water Elemental Intellect x:	0.3
            #Water Elemental +damage x:	0.4
            water_bolt_dmg = 521
            water_bolt_dmg += 0.4*mod_stats['actual_spellpower']['frost']
            crit_chance = 0.02*talents['winters_chill'] #np.min([(stats['crit_chance']+), stats['actual_hit'][self.school]] )
            #print([(stats['crit_chance']+self.crit_chance_talent_modifier), stats['actual_hit'][self.school]] )
            #print(crit_chance, stats['crit_chance'],self.crit_chance_talent_modifier, self.school)
            crit_bonus = 0.05+water_bolt_dmg*0.5*crit_chance
            # apparently it is a two-roll system
            #crit_bonus = crit_bonus/(1-0.17) # this is a one-roll system, a crit is guaranteed to hitif 'arcane_blast_1_0speed_0mana' == self.name:
            average_damage = water_bolt_dmg + crit_bonus
            average_damage*=game_config['partial_resist_multiplier']
            average_damage*=1-0.17
            water_elemental_dps = average_damage/2.5
            add_damage = np.ones(times.shape)*add_damage
            WE_times = copy.deepcopy(times)
            WE_times[WE_times>45] = 45
            add_damage += WE_times*water_elemental_dps
            #add_damage += spell.average_damage # wrong because it assumes WE gets buffs from talents
            base_manas -= spell.actual_mana
            times_mod -= spell.actual_cast_time # the casttime is 1.5, but you sacrifice 1s because you do not use POM for AB
            if not talents['disable_cold_snap']:
                WE_times = copy.deepcopy(times)-45
                WE_times[WE_times>45] = 45
                WE_times[WE_times<0] = 0
                add_damage += WE_times*water_elemental_dps
                #add_damage += spell.average_damage
                base_manas -= spell.actual_mana
                times_mod -= spell.actual_cast_time # the casttime is 1.5, but you sacrifice 1s because you do not use POM for AB
    mana_shift_evo = 0
    for _ in range (4):
        # the iterations here calculate the differences in mana from the intital guess to the actual mana spent given:
        #1. if the rotation does not work duing IV
        #2. there is a mana discount from AB spam during AP since the 1.3x mana only acts on the base mana
        manas_evo = base_manas+stats['mana']*0.6 +mana_shift_evo# include evocation
        times_evo = times_mod-8 # include evocation
        damage_evo, damage_burn_evo, damage_save_evo = find_damage(times_evo, manas_evo, expensive_rot, cheap_rot)
        mana_shift_evo = 0
        if not type(IV_replace) == type(None) and 1:
            overshoot_time = IVtime-damage_burn_evo/expensive_rot[0]
            overshoot_time[overshoot_time<0] = 0
            damage_evo+= overshoot_time*(IV_replace[0]-cheap_rot[0])
            damage_save_evo +=overshoot_time*(IV_replace[0]-cheap_rot[0])
            mana_shift_evo += -overshoot_time*(IV_replace[1]-cheap_rot[1])
            #print(overshoot_time)

        if talents['arcane_power']:
            # i here assume the burn rotation is pure AB spam
            AB_AP_uptime = damage_burn_evo/expensive_rot[0]
            AB_AP_uptime[AB_AP_uptime>15*1.3]=15*1.3
            mana_shift_evo += AB_AP_uptime *0.3* 195*(0+0.75*3)/1.5

    mana_shift_no_evo = 0
    for _ in range (4):
        # the iterations here calculate the differences in mana from the intital guess to the actual mana spent given:
        #1. if the rotation does not work duing IV
        #2. there is a mana discount from AB spam during AP since the 1.3x mana only acts on the base mana

        manas_no_evo =  base_manas + mana_shift_no_evo
        times_no_evo = times_mod
        damage_no_evo, damage_burn_no_evo, damage_save_no_evo = find_damage(times_no_evo, manas_no_evo, expensive_rot, cheap_rot)
        mana_shift_no_evo = 0
        if not type(IV_replace) == type(None) and 1:
            overshoot_time = IVtime-damage_burn_no_evo/expensive_rot[0]
            overshoot_time[overshoot_time<0] = 0
            damage_no_evo+= overshoot_time*(IV_replace[0]-cheap_rot[0])
            damage_save_no_evo+=overshoot_time*(IV_replace[0]-cheap_rot[0])
            mana_shift_no_evo += -overshoot_time*(IV_replace[1]-cheap_rot[1])
            #print(overshoot_time*(IV_replace[1]-cheap_rot[1]))
        if talents['arcane_power']:
            # i here assume the burn rotation is pure AB spam
            AB_AP_uptime = damage_burn_no_evo/expensive_rot[0]
            AB_AP_uptime[AB_AP_uptime>15*1.3]=15*1.3
            mana_shift_no_evo += AB_AP_uptime *0.3* 195*(0+0.75*3)/1.5
    #print(mana_shift_no_evo)
    # find best, evo/no evo
    damage = damage_evo
    damage_burn = damage_burn_evo
    damage_save = damage_save_evo
    for i,_ in enumerate(damage):
        if damage_no_evo[i]>damage_evo[i]:
            damage[i] = damage_no_evo[i]
            damage_burn[i] = damage_burn_no_evo[i]
            damage_save[i] = damage_save_no_evo[i]
    damage += add_damage
    if return_fractions:
        return damage, damage_burn, damage_save, add_damage, times_mod[0]
    return damage

def get_dps_mps_rot_clearcasting_optimal(stats, talents, game_config, spells_to_cast = 10000):
    np.random.seed(42)
    talents['force_clearcasting'] = -1
    spells_no_c, stats_no_c = get_spells_stats(stats, talents, game_config)
    talents['force_clearcasting'] = 1
    spells_forced_c, stats_forced_c = get_spells_stats(stats, talents, game_config)
    talents['force_clearcasting'] = 0 # reset

    global rot_mana, rot_damage,rot_time, time_since_last_stack,ab_stack

    rot_mana = 0
    rot_damage = 0
    rot_time = 0

    ab_stack = 0
    time_since_last_stack = 10
    clearcasting = 1
    #three_ab_am_scorch_rot = ['arcane_blast_1_3speed_0mana','arcane_blast_1_1speed_1mana','arcane_blast_1_2speed_2mana','arcane_missiles_10','scorch_9' ]
    def cast_spell(spell):
        global rot_mana, rot_damage,rot_time, time_since_last_stack,ab_stack
        rot_mana += spell.actual_mana
        rot_damage += spell.average_damage
        rot_time += spell.actual_cast_time
    while spells_to_cast>0:
        spells_to_cast-=1
        if clearcasting and time_since_last_stack<5:
            cast_spell(spells_forced_c['arcane_missiles_10'])
            time_since_last_stack += 5
        elif time_since_last_stack == 5:
            if clearcasting:
                cast_spell(spells_forced_c['frostbolt_13'])
            else:
                cast_spell(spells_no_c['frostbolt_13'])
            time_since_last_stack += 2.5
        elif ab_stack == 0:
            if clearcasting:
                spell = spells_forced_c['arcane_blast_1_0speed_0mana']
            else:
                spell = spells_no_c['arcane_blast_1_0speed_0mana']
            cast_spell(spell)
            ab_stack = 1
            time_since_last_stack = 0
        elif ab_stack == 1:
            if clearcasting:
                spell = spells_forced_c['arcane_blast_1_1speed_1mana']
            else:
                spell = spells_no_c['arcane_blast_1_1speed_1mana']
            if time_since_last_stack + spell.actual_cast_time >= 8:
                if clearcasting:
                    spell = spells_forced_c['arcane_blast_1_1speed_0mana']
                else:
                    spell = spells_no_c['arcane_blast_1_1speed_0mana']
                ab_stack = 1
            else:
                ab_stack = 2
            cast_spell(spell)
            time_since_last_stack = 0
        elif ab_stack == 2:
            if clearcasting:
                spell = spells_forced_c['arcane_blast_1_2speed_2mana']
            else:
                spell = spells_no_c['arcane_blast_1_2speed_2mana']
            if time_since_last_stack + spell.actual_cast_time >= 8:
                if clearcasting:
                    spell = spells_forced_c['arcane_blast_1_2speed_0mana']
                else:
                    spell = spells_no_c['arcane_blast_1_2speed_0mana']
                ab_stack = 1
            else:
                ab_stack = 3
            cast_spell(spell)
            time_since_last_stack = 0
        elif ab_stack == 3 and time_since_last_stack == 7.5:
            if clearcasting:
                spell = spells_forced_c['arcane_blast_1_3speed_0mana']
            else:
                spell = spells_no_c['arcane_blast_1_3speed_0mana']
            cast_spell(spell)
            time_since_last_stack = 0
            ab_stack = 1
        elif ab_stack == 3:
            if clearcasting:
                cast_spell(spells_forced_c['frostbolt_13'])
            else:
                cast_spell(spells_no_c['frostbolt_13'])
            time_since_last_stack += 2.5
            '''else:
            cast_spell(spells_no_c['arcane_missiles_10'])
            time_since_last_stack += 5'''
        if np.random.random() < 0.1:
            clearcasting = 1
        else:
            clearcasting = 0
        if time_since_last_stack>=8:
            ab_stack = 0
        #print(time_since_last_stack, ab_stack,clearcasting )

    dps = rot_damage/rot_time
    mps = rot_mana/rot_time
    return dps, mps

def get_dps_mps_spam_clearcasting_optimal(stats, talents, game_config, spells_to_cast = 10000):
    np.random.seed(1)
    talents['force_clearcasting'] = -1
    spells_no_c, stats_no_c = get_spells_stats(stats, talents, game_config)
    talents['force_clearcasting'] = 1
    spells_forced_c, stats_forced_c = get_spells_stats(stats, talents, game_config)
    talents['force_clearcasting'] = 0 # reset

    global rot_mana, rot_damage,rot_time, time_since_last_stack,ab_stack

    rot_mana = 0
    rot_damage = 0
    rot_time = 0

    ab_stack = 0
    time_since_last_stack = 10
    clearcasting = 1
    def cast_spell(spell):
        global rot_mana, rot_damage,rot_time, time_since_last_stack,ab_stack
        rot_mana += spell.actual_mana
        rot_damage += spell.average_damage
        rot_time += spell.actual_cast_time
    while spells_to_cast>0:
        spells_to_cast-=1
        if clearcasting:
            cast_spell(spells_forced_c['arcane_missiles_10'])
        else:
            spell = spells_no_c['arcane_blast_1_3speed_3mana']
            cast_spell(spell)
        if np.random.random() < 0.1:
            clearcasting = 1
        else:
            clearcasting = 0
        #print(time_since_last_stack, ab_stack,clearcasting )

    dps = rot_damage/rot_time
    mps = rot_mana/rot_time
    return dps, mps

def buff_me(stats, talents, buffs):
    talents['misc_add_mana'] = 0
    talents['innervate'] = 0
    talents['curse_of_shadow'] = 0 # +10% more damage from arcane
    talents['curse_of_elements'] = 0 # +10% more damage from fire/frost
    talents['malediction'] = 0 # +3% more damage from curse of elements/shadow
    talents['mage armor'] = 0 # +30 % mana regen
    talents['shadow_priest_dps'] = 0 # you get 5% of this as mana
    talents['2_tier5_set_bonus'] = 0 # 20% increase of mana cost and damage of AB
    talents['misery'] = 0 # 5 % more damage (shadow priest)

    for buff in buffs:
        val = buffs[buff]
        # things that are 'stats'
        if buff == 'arcane_intellect':
            stats['intellect'] += 40*val
        if buff == 'molten_armor':
            stats['crit_rating'] += 3*22.1*val # +3% crit
        if buff == 'divine_spirit':
            stats['spirit'] += 50*val #
        if buff == 'wrath_of_air_totem': # 102 spelldamage
            stats['common_spell_damage'] += 102*val
        if buff == 'improved_wrath_of_air_totem':
            stats['common_spell_damage'] += 20*val
        if buff == 'totem_of_wrath':# +3% hit and +3% crit
            stats['hit_rating'] += 3*12.6*val
            stats['crit_rating'] += 3*22.1*val
        if buff == 'mark_of_the_wild':
            if 'improved_mark_of_the_wild' in buffs and buffs['improved_mark_of_the_wild']==1:
                stats['intellect'] += 14*val*1.35
                stats['spirit'] += 14*val*1.35
            else:
                stats['intellect'] += 14*val
                stats['spirit'] += 14*val
        # things as 'talents'
        if buff == 'misc_add_mana':
            talents['misc_add_mana'] = val # super mana potion 2400, mana Emerald 2400, etc
        if buff == 'innervate':
            talents['innervate'] = val # 400 % mana regen for 400 s
        if buff == 'curse_of_shadow':
            talents['curse_of_shadow'] = val # +10% more damage from arcane
        if buff == 'curse_of_elements':
            talents['curse_of_elements'] = val # +10% more damage from fire/frost
        if buff == 'malediction':
            talents['malediction'] = val # +3% more damage from curse of elements/shadow
        if buff == 'misery':
            talents['misery'] = val
        if buff == 'mage_armor':
            talents['mage_armor'] = val # +30 % mana regen
        if buff == 'shadow_priest_dps':
            talents['shadow_priest_dps'] = val # you get 5% of this as mana
        if buff == '2_tier5_set_bonus':
            talents['2_tier5_set_bonus'] = val # 20% increase of mana cost and damage of AB
        if buff == 'spellfire_set':
            talents['spellfire_set'] = val # Increases spell damage by up to 7% of your total Intellect.
        if buff == 'judgement_of_wisdom':
            talents['judgement_of_wisdom'] = val # 50% chance to return 74 mana


    # these buffs need to be applied last
    for buff in buffs:
        val = buffs[buff]
        if buff == 'blessing_of_kings':# int/sim *= 1.1
            stats['intellect'] *= 1+0.1*val
            stats['spirit'] *= 1+0.1*val
        if buff == 'blessing_of_wisdom':# int/sim *= 1.1
            stats['mp5'] += 41*val

    for buff in buffs:
        val = buffs[buff]
        if buff == 'improved_divine_spirit':
            stats['common_spell_damage'] += 0.1*stats['spirit']*val



def get_damages_different_spec(times, base_stats, buffs, basic_rotation_rot = None, verbose= False):
    import copy
    # make talents
    fire_stats = copy.deepcopy(base_stats)
    fire_talents = make_fire_talents()
    buff_me(fire_stats, fire_talents, buffs)
    fire_spells, fire_stats = get_spells_stats(fire_stats, fire_talents, game_config)
    #print('made fire')
    arcane_stats_0 = copy.deepcopy(base_stats)
    arcane_talents = make_arcane_frost_talents()
    buff_me(arcane_stats_0, arcane_talents, buffs)
    arcane_spells, arcane_stats = get_spells_stats(arcane_stats_0, arcane_talents, game_config)
    #print(arcane_stats['intellect'])
    #print(arcane_stats['spirit'])
    #print('made arcane')

    # fire rotation
    fire_fireball_spam = get_dps_mps_rotation([fire_spells['fireball_13_one_tick']])
    four_fireball_one_scorch_spam_rot = ['fireball_13_one_tick','fireball_13_one_tick','fireball_13_one_tick','fireball_13_two_tick','scorch_9' ]
    four_fireball_one_scorch_spam = get_dps_mps_rotation([fire_spells[x] for x in four_fireball_one_scorch_spam_rot])

    # arcane ab spam
    ab_spam = get_dps_mps_rotation([arcane_spells['arcane_blast_1_3speed_3mana']])
    #print(ab_spam)
    #ab_spam = get_dps_mps_spam_clearcasting_optimal(arcane_stats, arcane_talents, game_config)
    # arcane basic rotation
    if type(basic_rotation_rot) == type(None):
        basic_rotation_rot = ['arcane_blast_1_3speed_0mana','arcane_blast_1_1speed_1mana','arcane_blast_1_2speed_2mana','frostbolt_13','frostbolt_13','frostbolt_13' ]
    basic_rotation = get_dps_mps_rotation([arcane_spells[x] for x in basic_rotation_rot])

    clearcasting_optimized = get_dps_mps_rot_clearcasting_optimal(arcane_stats_0, arcane_talents, game_config)

    ################# calculate optimal sycles
    arcane_damage, damage_burn_base, damage_save_base, _0, _1 = optimize_cycles_return_damage(arcane_stats,times,arcane_talents, ab_spam, basic_rotation, return_fractions=True )
    arcane_damage_clearcasting_optimized, damage_burn_optimal, damage_save_optimal, arcane_burn_rot, arcane_save_rot = optimize_cycles_return_damage(arcane_stats,times,arcane_talents, ab_spam, clearcasting_optimized, return_fractions=True )

    fireball_spam_damage, _0,_1,_2, fire_rot = optimize_cycles_return_damage(fire_stats,times,fire_talents, [0,10**10], fire_fireball_spam, return_fractions=True )

    if verbose:
        print('fire dps', fire_rot[0])
        print('arcane burn dps', arcane_burn_rot[0])
        print('arcane save dps', arcane_save_rot[0])


    four_fireball_one_scorch_damage = optimize_cycles_return_damage(fire_stats,times,fire_talents, [0,10**10], four_fireball_one_scorch_spam)
    return arcane_damage, arcane_damage_clearcasting_optimized,fireball_spam_damage,four_fireball_one_scorch_damage, arcane_spells, fire_spells, damage_burn_base, damage_save_base, damage_burn_optimal, damage_save_optimal
