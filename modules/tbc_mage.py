import fns
import numpy as np
import sys
def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)
from .libs import tbc_mage_backend as bck
import importlib
importlib.reload(bck)
def read_stat_file(location, file, stats):
	loc = '/'.join(location.split('/')[:-1])+'/'+file
	with open(loc) as f:
		#print('stats for '+location+': '+loc)
		for line in f:
			if '#' in line:
				line = line.split('#')[0]
			sp = line.split()
			if len(sp)>1:
				if not sp[0][0] == '#':
					if sp[0] == 'intellect':
						stats['intellect'] = float(sp[1].strip())
					if sp[0] == 'spirit':
						stats['spirit'] = float(sp[1].strip())
					if sp[0] == 'common_spell_damage':
						stats['common_spell_damage'] = float(sp[1].strip())
					if sp[0] == 'crit_rating':
						stats['crit_rating'] = float(sp[1].strip())
					if sp[0] == 'hit_rating':
						stats['hit_rating'] = float(sp[1].strip())
					if sp[0] == 'mp5':
						stats['mp5'] = float(sp[1].strip())
					if sp[0] == 'fire_damage':
						stats['fire_damage'] = float(sp[1].strip())
					if sp[0] == 'frost_damage':
						stats['frost_damage'] = float(sp[1].strip())
					if sp[0] == 'arcane_damage':
						stats['arcane_damage'] = float(sp[1].strip())
					if sp[0] == 'haste_rating':
						stats['haste_rating'] = float(sp[1].strip())

class mage_file:
	def __init__(self,location):
		self.location= location
		self.label = 'no label'
		self.stats = {}
		self.talents = bck.make_talents()
		self.burn_rot = []
		self.save_rot = []
		with open(location) as f:
			for line in f:
				if '#' in line:
					line = line.split('#')[0]
				sp = line.split()
				if len(sp)>1:
					if not sp[0][0] == '#':
						if sp[0] == 'stats_file':
							read_stat_file(location, sp[1], self.stats)
						if sp[0] == 'intellect':
							self.stats['intellect'] = float(sp[1].strip())
						if sp[0] == 'spirit':
							self.stats['spirit'] = float(sp[1].strip())
						if sp[0] == 'common_spell_damage':
							self.stats['common_spell_damage'] = float(sp[1].strip())
						if sp[0] == 'crit_rating':
							self.stats['crit_rating'] = float(sp[1].strip())
						if sp[0] == 'hit_rating':
							self.stats['hit_rating'] = float(sp[1].strip())
						if sp[0] == 'mp5':
							self.stats['mp5'] = float(sp[1].strip())
						if sp[0] == 'fire_damage':
							self.stats['fire_damage'] = float(sp[1].strip())
						if sp[0] == 'frost_damage':
							self.stats['frost_damage'] = float(sp[1].strip())
						if sp[0] == 'arcane_damage':
							self.stats['arcane_damage'] = float(sp[1].strip())
						if sp[0] == 'haste_rating':
							self.stats['haste_rating'] = float(sp[1].strip())
						for talent in self.talents:
							if sp[0] == talent:
								self.talents[talent] = int(sp[1].strip())
						if sp[0] == 'burn_rotation:':
							for i in range(1,len(sp)):
								self.burn_rot.append(sp[i])
						if sp[0] == 'save_rotation:':
							for i in range(1,len(sp)):
								self.save_rot.append(sp[i])
						if sp[0] == 'label':
							self.label = ' '.join(sp[1:])
						if sp[0] == 'color':
							self.color = [0,0,0,1]
							self.color[0] = float(sp[1])
							self.color[1] = float(sp[2])
							self.color[2] = float(sp[3])

def parse_rot(rot):
	new_rot =[]
	l = len(rot)
	for i, spell in enumerate(rot):
		if spell == 'fireball':
			pos_ign = 0
			if rot[(i+1)%l] == 'fireball':
				pos_ign +=1
				if rot[(i+2)%l] == 'fireball':
					pos_ign +=1
				elif rot[(i+2)%l] == 'scorch' and rot[(i+3)%l] == 'scorch':
					pos_ign +=1
			elif rot[(i+1)%l] == 'scorch' and rot[(i+2)%l] == 'scorch':
				pos_ign +=1
				if rot[(i+3)%l] == 'fireball':
					pos_ign +=1
				elif rot[(i+3)%l] == 'scorch' and rot[(i+4)%l] == 'scorch':
					pos_ign +=1
			if pos_ign == 2:
				new_rot.append('fireball_13_one_tick')
			elif pos_ign == 1:
				new_rot.append('fireball_13_one_tick_one_roll')
			elif pos_ign == 0:
				new_rot.append('fireball_13_one_tick_no_roll')

		elif spell == 'scorch':
			pos_ign = 0
			if rot[(i+1)%l] == 'fireball':
				pos_ign +=1
				if rot[(i+2)%l] == 'fireball':
					pos_ign +=1
				elif rot[(i+2)%l] == 'scorch' and rot[(i+3)%l] == 'scorch':
					pos_ign +=1
			elif rot[(i+1)%l] == 'scorch' and rot[(i+2)%l] == 'scorch':
				pos_ign +=1
				if rot[(i+3)%l] == 'fireball':
					pos_ign +=1
				elif rot[(i+3)%l] == 'scorch' and rot[(i+4)%l] == 'scorch':
					pos_ign +=1
			if pos_ign == 2:
				new_rot.append('scorch_9')
			elif pos_ign == 1:
				new_rot.append('scorch_9_one_roll')
			elif pos_ign == 0:
				new_rot.append('scorch_9_no_roll')
			new_rot.append('scorch_9')
		elif spell == 'fireblast':
			new_rot.append('fireblast')
		elif spell == 'arcane_missiles':
			new_rot.append('arcane_missiles_10')
		elif spell == 'frostbolt':
			new_rot.append('frostbolt_13')
		elif spell == 'arcane_blast_0speed_0mana':
			new_rot.append('arcane_blast_1_0speed_0mana')
		elif spell == 'arcane_blast_1speed_1mana':
			new_rot.append('arcane_blast_1_1speed_1mana')
		elif spell == 'arcane_blast_2speed_2mana':
			new_rot.append('arcane_blast_1_2speed_2mana')
		elif spell == 'arcane_blast_3speed_3mana':
			new_rot.append('arcane_blast_1_3speed_3mana')
		elif spell == 'arcane_blast_1speed_0mana':
			new_rot.append('arcane_blast_1_1speed_0mana')
		elif spell == 'arcane_blast_2speed_0mana':
			new_rot.append('arcane_blast_1_2speed_0mana')
		elif spell == 'arcane_blast_3speed_0mana':
			new_rot.append('arcane_blast_1_3speed_0mana')
		else:
			print('spell '+ spell+ ' not found, possible spells are:')
			pos_spells = ['fireball_13_one_tick',
				'fireball',
				'scorch',
				'fireblast',
				#'pyroblast',
				#'pom_pyroblast',
				'arcane_missiles',
				'arcane_blast_0speed_0mana',
				'arcane_blast_1speed_1mana',
				'arcane_blast_2speed_2mana',
				'arcane_blast_3speed_3mana',
				'arcane_blast_1speed_0mana',
				'arcane_blast_2speed_0mana',
				'arcane_blast_3speed_0mana',
				'frostbolt',
			]
			for spell in pos_spells:
				print(spell)
	return new_rot

class moduleClass:
	filetypes=['mage']
	def __init__ (self, fig, locations, frame, ui):
		self.fig=fig
		self.frame=frame
		self.locations=locations
		self.ui=ui
	def run(self):

		if self.ui['save_check']:
			try:
				import os
				os.makedirs(self.ui['save_filename'])
			except:
				None
		ui=self.ui
		fig=self.fig
		#prepare figure
		fig.clear()
		#load mages
		mage_colors = [[0.5,0,1,1],
						[1,0.5,0,1],
						[0.2,0.2,1,1],
						[0,0,0,1],
						[0.5,0,1,1],
						[1,1,0,1],
						[0.2,1,1,1],
						[0,1,0,1],
						]
		self.mages=[]
		for i, location in enumerate(self.locations):
			self.mages.append(mage_file(location))
			if self.mages[-1].save_rot[0] == 'arcane_frost_clearcasting_optimized':
				None
			elif self.mages[-1].save_rot[0] == 'fireball_spam_clearcasting_optimized':
				None
			elif self.mages[-1].save_rot[0] == 'frostbolt_spam_clearcasting_optimized':
				None
			elif self.mages[-1].save_rot[0] == 'scorch_spam_clearcasting_optimized':
				None
			else:
				self.mages[-1].save_rot = parse_rot(self.mages[-1].save_rot)
			if self.mages[-1].burn_rot[0] == 'None':
				None
			elif self.mages[-1].burn_rot[0] == 'AB_spam_clearcasting_optimized':
				None
			else:
				self.mages[-1].burn_rot = parse_rot(self.mages[-1].burn_rot)
			if not hasattr(self.mages[-1],'color'):
				self.mages[-1].color = mage_colors[i%8]
			for key in ['disable_arcane_power', 'disable_icy_veins', 'disable_cold_snap', 'disable_water_elemental', 'disable_combustion', 'disable_PoM_pyro', 'ignore_scorch_ramp']:
				self.mages[-1].talents[key] = ui[key]
		#load buffs
		buff_cases = []
		for i in range(5):
			#merge coe and cos, as in patch 2.4(?)
			ui['buff_case_'+str(i)+'_curse_of_shadow'] = ui['buff_case_'+str(i)+'_curse_of_elements']
			buff_cases.append({})
			buff_case_str = 'buff_case_'+str(i)+'_'
			for key in ui:
				if buff_case_str in key:
					buff = key.split(buff_case_str)[1]
					try:
						buff_cases[i][buff] = int(ui[key])
					except:
						buff_cases[i][buff] = ui[key]
			if buff_cases[i]['armor'] == 'mage armor':
				buff_cases[i]['mage_armor'] = 1
				buff_cases[i]['molten_armor'] = 0
			else:
				buff_cases[i]['mage_armor'] = 0
				buff_cases[i]['molten_armor'] = 1
			#buttons.append({'key': 'buff_case_'+str(k)+'armor', 'type': 'radio:text', 'texts': ['molten armor', 'mage armor']','default': '0', 'tab': 1, 'row': i})
			#buttons.append({'key': 'buff_case_'+str(k)+'_molten_armor', 'type': 'check', 'text': 'molten armor','default': '1', 'tab': 1, 'row': i})
			#buttons.append({'key': 'buff_case_'+str(k)+'_mage_armor', 'type': 'check', 'text': 'mage armor','default': '0', 'tab': 1, 'row': i})

		#plot measurements
		linestyles=['-','-.','--',(0, (3, 1, 1, 1, 1, 1)),':']

		self.frame.hidden_figure.set_dpi(300)
		self.frame.hidden_figure.set_size_inches(8,4)
		#self.frame.update()
		#self.frame.figure.	canvas.draw()
		if ui['plot_dmg']:
			ax = fns.add_axis(self.fig,2)
			ax.grid()
			misc = []
			for i, buff_case in enumerate(buff_cases):
				linestyle = linestyles[i]
				if buff_case['check'] == 1:
					for mage in self.mages:
						misc = plot_dps(ui, mage, buff_case, i, linestyle, ax, misc, fractions = ui['include_rotation_fractions'], DMG = True)

			if ui['save_check']:
				misc = []
				self.frame.hidden_figure.clf()
				tempax = self.frame.hidden_figure.add_subplot(111)
				tempax.grid()
				for i, buff_case in enumerate(buff_cases):
					linestyle = linestyles[i]
					if buff_case['check'] == 1:
						for mage in self.mages:
							misc = plot_dps(ui, mage, buff_case, i, linestyle, tempax, misc, fractions = ui['include_rotation_fractions'], DMG = True)
				self.frame.hidden_figure.tight_layout()
				#print(self.frame.tempfig)
				self.frame.hidden_figure.savefig(ui['save_filename']+'/dmg.svg')
				self.frame.hidden_figure.savefig(ui['save_filename']+'/dmg.png')
		#self.frame.update()
		#self.frame.figure.canvas.draw()
		if ui['plot_dps']:
			ax = fns.add_axis(self.fig,2)
			ax.grid()
			misc = []
			for i, buff_case in enumerate(buff_cases):
				linestyle = linestyles[i]
				if buff_case['check'] == 1:
					for mage in self.mages:
						misc = plot_dps(ui, mage, buff_case, i, linestyle, ax, misc, fractions = ui['include_rotation_fractions'], DMG = False)

			if ui['save_check']:
				misc = []
				self.frame.hidden_figure.clf()
				tempax = self.frame.hidden_figure.add_subplot(111)
				tempax.grid()
				for i, buff_case in enumerate(buff_cases):
					linestyle = linestyles[i]
					if buff_case['check'] == 1:
						for mage in self.mages:
							misc = plot_dps(ui, mage, buff_case, i, linestyle, tempax, misc, fractions = ui['include_rotation_fractions'], DMG = False)
				self.frame.hidden_figure.tight_layout()
				#print(self.frame.tempfig)
				self.frame.hidden_figure.savefig(ui['save_filename']+'/dps.svg')
				self.frame.hidden_figure.savefig(ui['save_filename']+'/dps.png')
		#self.frame.update()
		#self.frame.figure.canvas.draw()
		if ui['plot_compare_buff_states']:
			num_buff_cases = 0
			for i, buff_case in enumerate(buff_cases):
				if buff_case['check'] == 1:
					num_buff_cases+=1
			if num_buff_cases>1:
				ax = fns.add_axis(self.fig,2)
				plot_compare_buff_states(ui, self.mages, buff_cases, linestyles, ax)
				if ui['save_check']:
					self.frame.hidden_figure.clf()
					tempax = self.frame.hidden_figure.add_subplot(111)
					plot_compare_buff_states(ui, self.mages, buff_cases, linestyles, tempax)
					self.frame.hidden_figure.tight_layout()
					#print(self.frame.tempfig)
					self.frame.hidden_figure.savefig(ui['save_filename']+'/comp_buff_states.svg')
					self.frame.hidden_figure.savefig(ui['save_filename']+'/comp_buff_states.png')
		if ui['plot_compare_mages']:
			if hasattr(self.frame,'default_mage'):
				default_mage=mage_file(self.frame.default_mage)
				if default_mage.save_rot[0] == 'arcane_frost_clearcasting_optimized':
					None
				elif default_mage.save_rot[0] == 'fireball_spam_clearcasting_optimized':
					None
				elif default_mage.save_rot[0] == 'frostbolt_spam_clearcasting_optimized':
					None
				elif default_mage.save_rot[0] == 'scorch_spam_clearcasting_optimized':
					None
				else:
					default_mage.save_rot = parse_rot(default_mage.save_rot)
				if default_mage.burn_rot[0] == 'None':
					None
				elif default_mage.burn_rot[0] == 'AB_spam_clearcasting_optimized':
					None
				else:
					default_mage.burn_rot = parse_rot(default_mage.burn_rot)
				if not hasattr(default_mage,'color'):
					default_mage.color = mage_colors[i%8]
				for key in ['disable_arcane_power', 'disable_icy_veins', 'disable_cold_snap', 'disable_water_elemental', 'disable_combustion', 'disable_PoM_pyro', 'ignore_scorch_ramp']:
					default_mage.talents[key] = ui[key]
				ax = fns.add_axis(self.fig,2)
				plot_compare_mages(ui, default_mage, self.mages, buff_cases, linestyles, ax)
				if ui['save_check']:
					self.frame.hidden_figure.clf()
					tempax = self.frame.hidden_figure.add_subplot(111)
					plot_compare_mages(ui, default_mage, self.mages, buff_cases, linestyles, tempax)
					self.frame.hidden_figure.tight_layout()
					#print(self.frame.tempfig)
					self.frame.hidden_figure.savefig(ui['save_filename']+'/comp_mages.svg')
					self.frame.hidden_figure.savefig(ui['save_filename']+'/comp_mages.png')
		if ui['plot_spell_dps']:
			ax = fns.add_axis(self.fig,2)
			plot_spell_dps(ui, self.mages, buff_cases, linestyles, ax)
			if ui['save_check']:
				self.frame.hidden_figure.clf()
				tempax = self.frame.hidden_figure.add_subplot(111)
				plot_spell_dps(ui, self.mages, buff_cases, linestyles, tempax)
				self.frame.hidden_figure.tight_layout()
				#print(self.frame.tempfig)
				self.frame.hidden_figure.savefig(ui['save_filename']+'/spell_dps.svg')
				self.frame.hidden_figure.savefig(ui['save_filename']+'/spell_dps.png')
		#self.frame.figure.canvas.draw()
		if ui['plot_spell_dpm']:
			ax = fns.add_axis(self.fig,2)
			plot_spell_dps(ui, self.mages, buff_cases, linestyles, ax, DPM= True)
			if ui['save_check']:
				self.frame.hidden_figure.clf()
				tempax = self.frame.hidden_figure.add_subplot(111)
				plot_spell_dps(ui, self.mages, buff_cases, linestyles, tempax, DPM= True)
				self.frame.hidden_figure.tight_layout()
				#print(self.frame.tempfig)
				self.frame.hidden_figure.savefig(ui['save_filename']+'/spell_dpm.svg')
				self.frame.hidden_figure.savefig(ui['save_filename']+'/spell_dpm.png')
		#self.frame.figure.canvas.draw()
		if ui['plot_stat_weights']:
			ax = fns.add_axis(self.fig,2)
			plot_stat_weights(ui, self.mages, buff_cases, linestyles, ax)
			if ui['save_check']:
				self.frame.hidden_figure.clf()
				tempax = self.frame.hidden_figure.add_subplot(111)
				plot_stat_weights(ui, self.mages, buff_cases, linestyles, tempax)
				self.frame.hidden_figure.tight_layout()
				#print(self.frame.tempfig)
				self.frame.hidden_figure.savefig(ui['save_filename']+'/stat_weights.svg')
				self.frame.hidden_figure.savefig(ui['save_filename']+'/stat_weights.png')
		'''
		ax.legend()
		#set x and ylabel
		ax.set_xlabel(ui['XYxlabel'])
		ax.set_xlim([ui['XYxmin'],ui['XYxmax']])
		ax.set_ylabel(ui['XYylabel'])
		'''
		if ui['save_check']:
			self.fig.savefig(ui['save_filename']+'/all.svg')
			self.fig.savefig(ui['save_filename']+'/all.png')
		fig.canvas.draw()
		self.frame.update()
	def addButtons():

		buttons=[
			{'key': 'mage_tab_0_name', 'type': 'tabname', 'text': 'misc', 'tab': 0} ,
			{'key': 'mage_tab_1_name', 'type': 'tabname', 'text': 'buffs', 'tab': 1} ,

			{'key': 'plot_dmg', 'type': 'check', 'text': 'plot_dmg','default': '1', 'tab': 0, 'row': 0},
			{'key': 'plot_dps', 'type': 'check', 'text': 'plot_dps','default': '1', 'tab': 0, 'row': 0},
			{'key': 'include_rotation_fractions', 'type': 'check', 'text': 'include rotation fractions','default': '0', 'tab': 0, 'row': 0},


			{'key': 'plot_compare_buff_states', 'type': 'check', 'text': 'plot_compare_buff_states','default': '1', 'tab': 0, 'row': 0},
			{'key': 'set_default_mage', 'type': 'click', 'text': 'set_default_mage','bind': set_default_mage, 'tab': 0, 'row': 0},
			{'key': 'plot_compare_mages', 'type': 'check', 'text': 'plot_compare_mages','default': '1', 'tab': 0, 'row': 0},
			#{'key': 'clear_default_mage', 'type': 'click', 'text': 'set_default_mage','bind': clear_default_mage, 'tab': 10, 'row': 0},
			{'key': 'plot_spell_dps', 'type': 'check', 'text': 'plot_spell_dps','default': '0', 'tab': 0, 'row': 0},
			{'key': 'plot_spell_dpm', 'type': 'check', 'text': 'plot_spell_dpm','default': '0', 'tab': 0, 'row': 0},

			{'key': 'plot_stat_weights', 'type': 'check', 'text': 'plot_stat_weights','default': '0', 'tab': 0, 'row': 0},


			{'key': 'time_min', 'type': 'txt:float', 'text': 'time_min', 'default': '40', 'width': 4, 'tab': 0, 'row': 1} ,
			{'key': 'time_max', 'type': 'txt:float', 'text': 'time_max', 'default': '180', 'width': 4, 'tab': 0, 'row': 1} ,
			{'key': 'dps_min', 'type': 'txt:float', 'text': 'dps_min', 'default': '0', 'width': 4, 'tab': 0, 'row': 2} ,
			{'key': 'dps_max', 'type': 'txt:float', 'text': 'dps_max', 'default': '2000', 'width': 4, 'tab': 0, 'row': 2} ,
			{'key': 'stat_weight_ymax', 'type': 'txt:int', 'text': 'stat_weight_ymax', 'default': '2', 'width': 4, 'tab': 0, 'row': 2} ,


			{'key': 'disable_arcane_power', 'type': 'check', 'text': 'disable_arcane_power','default': '0', 'tab': 0, 'row': 3},
			{'key': 'disable_icy_veins', 'type': 'check', 'text': 'disable_icy_veins','default': '0', 'tab': 0, 'row': 3},
			{'key': 'disable_cold_snap', 'type': 'check', 'text': 'disable_cold_snap','default': '0', 'tab': 0, 'row': 3},
			{'key': 'disable_water_elemental', 'type': 'check', 'text': 'disable_water_elemental','default': '0', 'tab': 0, 'row': 3},
			{'key': 'disable_combustion', 'type': 'check', 'text': 'disable_combustion','default': '0', 'tab': 0, 'row': 3},
			{'key': 'disable_PoM_pyro', 'type': 'check', 'text': 'disable_PoM_pyro','default': '0', 'tab': 0, 'row': 3},
			{'key': 'ignore_scorch_ramp', 'type': 'check', 'text': 'ignore_scorch_ramp','default': '0', 'tab': 0, 'row': 3},
		]
		j = len(buttons)
		for k in range(5):
			i=k*2
			buttons.append({'key': 'buff_case_'+str(k)+'_check', 'type': 'check', 'text': 'Buffs '+str(k),'default': '0', 'tab': 1, 'row': i})
			buttons.append({'key': 'buff_case_'+str(k)+'_label', 'type': 'txt', 'text': 'label:','default': 'buffs '+str(k), 'width': 10, 'tab': 1, 'row': i})
			buttons.append({'key': 'buff_case_'+str(k)+'_arcane_intellect', 'type': 'check', 'text': 'AI','default': '1', 'tab': 1, 'row': i})

			buttons.append({'key': 'buff_case_'+str(k)+'_armor', 'type': 'radio:text', 'texts': ['molten armor', 'mage armor'],'default': '0', 'tab': 1, 'row': i})
			#buttons.append({'key': 'buff_case_'+str(k)+'_molten_armor', 'type': 'check', 'text': 'molten armor','default': '1', 'tab': 1, 'row': i})
			#buttons.append({'key': 'buff_case_'+str(k)+'_mage_armor', 'type': 'check', 'text': 'mage armor','default': '0', 'tab': 1, 'row': i})
			buttons.append({'key': 'buff_case_'+str(k)+'_misc_add_mana', 'type': 'txt:float', 'text': '| misc mana (mana ruby, potions, etc)','default': '2400','width': 5, 'tab': 1, 'row': i})
			buttons.append({'key': 'buff_case_'+str(k)+'_innervate', 'type': 'txt:float', 'text': '# of innervates','default': '0','width': 2, 'tab': 1, 'row': i})

			buttons.append({'key': 'buff_case_'+str(k)+'_dummy_label', 'type': 'label', 'text': '               ', 'tab': 1, 'row': i+1})
					#{'key': 'XYxlabel', 'type': 'txt', 'text': 'x label', 'default': r'$2\theta$', 'width': 10, 'tab': 0, 'row': 1} ,
			#buttons.append({'key': 'buff_case_'+str(k)+'_curse_of_shadow', 'type': 'check', 'text': 'CoS','default': '1', 'tab': 1, 'row': i+1})
			buttons.append({'key': 'buff_case_'+str(k)+'_curse_of_elements', 'type': 'check', 'text': 'CoE','default': '1', 'tab': 1, 'row': i+1})
			buttons.append({'key': 'buff_case_'+str(k)+'_malediction', 'type': 'check', 'text': 'Malediction','default': '1', 'tab': 1, 'row': i+1})
			buttons.append({'key': 'buff_case_'+str(k)+'_divine_spirit', 'type': 'check', 'text': 'D.spirit','default': '1', 'tab': 1, 'row': i+1})
			buttons.append({'key': 'buff_case_'+str(k)+'_improved_divine_spirit', 'type': 'check', 'text': 'Imp.d.spirit','default': '1', 'tab': 1, 'row': i+1})
			buttons.append({'key': 'buff_case_'+str(k)+'_wrath_of_air_totem', 'type': 'check', 'text': 'WoA totem','default': '0', 'tab': 1, 'row': i+1})
			buttons.append({'key': 'buff_case_'+str(k)+'_improved_wrath_of_air_totem', 'type': 'check', 'text': 'imp.WoA','default': '0', 'tab': 1, 'row': i+1})
			buttons.append({'key': 'buff_case_'+str(k)+'_totem_of_wrath', 'type': 'check', 'text': 'totem of wrath','default': '0', 'tab': 1, 'row': i+1})
			buttons.append({'key': 'buff_case_'+str(k)+'_mark_of_the_wild', 'type': 'check', 'text': 'MotW','default': '1', 'tab': 1, 'row': i+1})
			buttons.append({'key': 'buff_case_'+str(k)+'_improved_mark_of_the_wild', 'type': 'check', 'text': 'imp.MotW','default': '1', 'tab': 1, 'row': i+1})
			buttons.append({'key': 'buff_case_'+str(k)+'_blessing_of_kings', 'type': 'check', 'text': 'BoK','default': '1', 'tab': 1, 'row': i+1})
			buttons.append({'key': 'buff_case_'+str(k)+'_blessing_of_wisdom', 'type': 'check', 'text': 'BoW','default': '1', 'tab': 1, 'row': i+1})
			buttons.append({'key': 'buff_case_'+str(k)+'_judgement_of_wisdom', 'type': 'check', 'text': 'JoW','default': '1', 'tab': 1, 'row': i+1})
			buttons.append({'key': 'buff_case_'+str(k)+'_shadow_priest_dps', 'type': 'txt:float', 'text': 'SP dps', 'default': '0', 'width': 4, 'tab': 1, 'row': i+1})
			buttons.append({'key': 'buff_case_'+str(k)+'_misery', 'type': 'check', 'text': 'misery','default': '0', 'tab': 1, 'row': i+1})
			buttons.append({'key': 'buff_case_'+str(k)+'_2_tier5_set_bonus', 'type': 'check', 'text': '2_tier5_set_bonus','default': '0', 'tab': 1, 'row': i+1})
			buttons.append({'key': 'buff_case_'+str(k)+'_spellfire_set', 'type': 'check', 'text': 'spellfire set','default': '0', 'tab': 1, 'row': i+1})

		buttons[j]['default'] = 1
		#{'key': 'XYxmin', 'type': 'txt:float', 'text': 'x min', 'default': '0', 'width': 4, 'tab': 0, 'row': 1} ,
		#{'key': 'XYxmax', 'type': 'txt:float', 'text': 'x max', 'default': '120', 'width': 4, 'tab': 0, 'row': 1} ,
		#{'key': 'XYxlabel', 'type': 'txt', 'text': 'x label', 'default': r'$2\theta$', 'width': 10, 'tab': 0, 'row': 1} ,
		#{'key': 'XYnormalize', 'type': 'check', 'text': 'Normalize y-axis', 'tab': 0, 'row': 2} ,
		#{'key': 'XYylabel_text', 'type': 'label', 'text': 'ylabel: ', 'tab': 0, 'row': 2} ,
		#{'key': 'XYylabel', 'type': 'radio:text', 'texts': ['Counts', 'Intensity'], 'tab': 0, 'row': 2,'default': 0} ,

		return buttons

import copy
def get_dmg(mage, buffs,times):
	new_stats_0 = copy.deepcopy(mage.stats)
	new_talents = copy.deepcopy(mage.talents)
	bck.buff_me(new_stats_0, new_talents, buffs)
	spells, new_stats = bck.get_spells_stats(new_stats_0, new_talents, bck.game_config)

	if mage.save_rot[0] == 'arcane_frost_clearcasting_optimized':
		save_rot = bck.get_dps_mps_rot_clearcasting_optimal(new_stats_0, new_talents, bck.game_config, spells_to_cast = 20000)
	elif mage.save_rot[0] == 'fireball_spam_clearcasting_optimized':
		new_talents['force_clearcasting'] = -1
		spells_no_c, stats_no_c = bck.get_spells_stats(new_stats_0, new_talents, bck.game_config)
		new_talents['force_clearcasting'] = 1
		spells_forced_c, stats_forced_c = bck.get_spells_stats(new_stats_0, new_talents, bck.game_config)
		new_talents['force_clearcasting'] = 0 # reset
		optimized_spells = [spells_no_c['fireball_13_one_tick']]*7
		optimized_spells.append(spells_no_c['fireball_13_one_tick_one_roll'])
		optimized_spells.append(spells_no_c['fireball_13_three_tick_no_roll'])
		optimized_spells.append(spells_forced_c['arcane_missiles_10'])
		save_rot = bck.get_dps_mps_rotation(optimized_spells)
	elif mage.save_rot[0] == 'scorch_spam_clearcasting_optimized':
		new_talents['force_clearcasting'] = -1
		spells_no_c, stats_no_c = bck.get_spells_stats(new_stats_0, new_talents, bck.game_config)
		new_talents['force_clearcasting'] = 1
		spells_forced_c, stats_forced_c = bck.get_spells_stats(new_stats_0, new_talents, bck.game_config)
		new_talents['force_clearcasting'] = 0 # reset
		optimized_spells = [spells_no_c['scorch_9']]*7
		optimized_spells.append(spells_no_c['scorch_9_no_roll'])
		optimized_spells.append(spells_no_c['scorch_9_no_roll'])
		optimized_spells.append(spells_forced_c['arcane_missiles_10'])
		save_rot = bck.get_dps_mps_rotation(optimized_spells)
	elif mage.save_rot[0] == 'frostbolt_spam_clearcasting_optimized':
		new_talents['force_clearcasting'] = -1
		spells_no_c, stats_no_c = bck.get_spells_stats(new_stats_0, new_talents, bck.game_config)
		new_talents['force_clearcasting'] = 1
		spells_forced_c, stats_forced_c = bck.get_spells_stats(new_stats_0, new_talents, bck.game_config)
		new_talents['force_clearcasting'] = 0 # reset
		optimized_spells = [spells_no_c['frostbolt_13']]*9
		optimized_spells.append(spells_forced_c['arcane_missiles_10'])
		save_rot = bck.get_dps_mps_rotation(optimized_spells)
	else:
		save_rot = bck.get_dps_mps_rotation([spells[x] for x in mage.save_rot])


	if mage.burn_rot[0] == 'None':
		burn_rot = [0,10**10]
	elif mage.burn_rot[0] == 'AB_spam_clearcasting_optimized':
		new_talents['force_clearcasting'] = -1
		spells_no_c, stats_no_c = bck.get_spells_stats(new_stats_0, new_talents, bck.game_config)
		new_talents['force_clearcasting'] = 1
		spells_forced_c, stats_forced_c = bck.get_spells_stats(new_stats_0, new_talents, bck.game_config)
		new_talents['force_clearcasting'] = 0 # reset
		optimized_spells = [spells_no_c['arcane_blast_1_3speed_3mana']]*9
		optimized_spells.append(spells_forced_c['arcane_missiles_10'])
		burn_rot = bck.get_dps_mps_rotation(optimized_spells)
	else:
		burn_rot = bck.get_dps_mps_rotation([spells[x] for x in mage.burn_rot])

	IV_replace = None
	if 'arcane_frost_clearcasting_optimized' in mage.save_rot or 'arcane_blast_1_3speed_0mana' in mage.save_rot:
		#print(mage.location)
		IV_replace = bck.get_dps_mps_rotation([spells[x] for x in ['frostbolt_13']])
	dmg, dmg_burn, dmg_save, dmg_other, time_shift = bck.optimize_cycles_return_damage(new_stats,times,new_talents, burn_rot, save_rot, return_fractions=True, IV_replace=IV_replace )

	return dmg, dmg_burn, dmg_save, dmg_other, time_shift

def plot_dps(ui, mage, buffs, i, linestyle, ax, misc, fractions = False, DMG = False):
	times = np.arange(ui['time_min'],ui['time_max']+1, 1)

	dmg, dmg_burn, dmg_save, dmg_other, time_shift = get_dmg(mage, buffs, times)
	if DMG:
		times_mod = 1
		ax.set_ylabel('Damage [DMG]')
		#ax.set_ylim([u,ui['dps_max']])
	else:
		times_mod = times
		ax.set_ylabel('Average dps [DMG/s]')
		ax.set_ylim([ui['dps_min'],ui['dps_max']])
	if fractions:
		if not 'dmg_frac_label' in misc:
			misc.append('dmg_frac_label')
			ax.fill_between(times,
							np.zeros(len(times)),
							dmg_save/times_mod,
							color=[0.5,0,1,0.2], label = 'save')
			ax.fill_between(times,
							dmg_save/times_mod,
							dmg_save/times_mod+dmg_burn/times_mod,
							color=[1,0,0.5,0.2], label = 'burn')
		else:
			ax.fill_between(times,
							np.zeros(len(times)),
							dmg_save/times_mod,
							color=[0.5,0,1,0.2])
			ax.fill_between(times,
							dmg_save/times_mod,
							dmg_save/times_mod+dmg_burn/times_mod,
							color=[1,0,0.5,0.2])

		if np.sum(dmg_other)>1000:
			if not 'dmg_frac_other_label' in misc:
				misc.append('dmg_frac_other_label')
				ax.fill_between(times,
								dmg_save/times_mod+dmg_burn/times_mod,
								dmg_save/times_mod+dmg_burn/times_mod+dmg_other/times_mod,
								color=[0,0,0,0.2], label = 'other (pom+pyro, etc)')
			else:
				ax.fill_between(times,
								dmg_save/times_mod+dmg_burn/times_mod,
								dmg_save/times_mod+dmg_burn/times_mod+dmg_other/times_mod,
								color=[0,0,0,0.2])

	ax.plot(times, dmg/times_mod, linestyle= linestyle, color=mage.color, label = mage.label+', '+ui['buff_case_'+str(i)+'_label'])
	ax.set_xticks(ticks=np.arange((int((times[0]-1)/30)+1)*30,times[-1]+1,30))
	ax.set_xlabel('Total casting time before boss dead [s]')
	'''ax.annotate('Evocation', xy=(43, 1100),
				xytext=(48, 1400),
				arrowprops=dict(facecolor='black', shrink=0.05),
				horizontalalignment='left', verticalalignment='top',
				)
	ax.annotate('OOM', xy=(110, 800),
				xytext=(120,1100),
				arrowprops=dict(facecolor='black', shrink=0.05),
				horizontalalignment='left', verticalalignment='top',
				)'''
	ax.legend()
	ax.set_xlim([ui['time_min'],ui['time_max']])
	ylim = ax.get_ylim()
	if ylim[0]<0:
		ax.set_ylim([0,ylim[1]])

	#fig.savefig('optimized_spam.png')
	return misc

def plot_spell_dps(ui, mages, buff_cases, linestyles, ax, DPM = False):
	#ax.grid()
	spell_names = ['frostbolt_13','fireball_13_one_tick',
				'scorch_9',
				'arcane_blast_1_0speed_0mana',
				'arcane_blast_1_1speed_1mana',
				'arcane_blast_1_2speed_2mana',
				'arcane_blast_1_3speed_3mana',
				'arcane_blast_1_3speed_0mana',
				'arcane_missiles_10',
				]
	x = np.arange(len(spell_names))
	tot_cases = 0
	for i, buff_case in enumerate(buff_cases):
		if buff_case['check'] == 1:
			tot_cases+=len(mages)
	j=0
	width = 0.8/(tot_cases)
	for i, buff_case in enumerate(buff_cases):
		linestyle = linestyles[i]
		if buff_case['check'] == 1:
			for mage in mages:
				new_stats_0 = copy.deepcopy(mage.stats)
				new_talents = copy.deepcopy(mage.talents)
				bck.buff_me(new_stats_0, new_talents, buff_case)
				spells, new_stats = bck.get_spells_stats(new_stats_0, new_talents, bck.game_config)

				dpms = []
				dpss = []
				for spell_name in spell_names:
					dps = spells[spell_name].average_damage / spells[spell_name].actual_cast_time
					dpss.append(dps)
					dpm = spells[spell_name].average_damage / spells[spell_name].actual_mana
					dpms.append(dpm)
				offset = -0.8/2+(j+0.5)*0.8/(tot_cases)
				color = [mage.color[0], mage.color[1], mage.color[2],0.5]
				edgecolor = [mage.color[0], mage.color[1], mage.color[2],1]
				if not DPM:
					rects = ax.bar(x +offset, dpss, width, linestyle=linestyle, edgecolor= edgecolor, color=color, label=mage.label)
				else:
					rects = ax.bar(x +offset, dpms, width, linestyle=linestyle, edgecolor= edgecolor, color=color, label=mage.label)
				#rects = ax[1].bar(x +offset, dpms, width, color=mage.color, label=mage.label)

				j+=1

	if not DPM:
		ax.set_ylabel('spell dps')
	else:
		ax.set_ylabel('spell dpm')
	#ax.set_ylabel('spell dpm')
	spell_names_short = ['Frostbolt',
			  'Fireball',
	          'Scorch',
	          'AB0',
	          'AB1',
	          'AB2',
	          'AB3',
	          'AB3\ncost1',
	          'AM',
	         ]
	ax.set_xticks(np.arange(0,len(spell_names_short),1))
	ax.set_xticklabels(spell_names_short)
	#ax[1].legend()
	#fig.tight_layout()
	return


def plot_stat_weights(ui, mages, buff_cases, linestyles, ax, DPM = False):
	stats_list = ['intellect','common_spell_damage',
					'crit_rating','hit_rating','haste_rating','mp5','spirit']
	stats_names = ['Intellect','+Spelldamage','Crit rating',
					'Hit rating','Haste','mp5','Spirit']
	x_step = ui['time_max']-ui['time_min']
	xlim = [ui['time_min'],ui['time_max']+3*x_step]
	times = np.arange(ui['time_min'],ui['time_max']+1, 1)
	max_ylim = ui['stat_weight_ymax']

	for i, buff_case in enumerate(buff_cases):
		linestyle = linestyles[i]
		if buff_case['check'] == 1:
			for mage in mages:
				tmp = get_dmg(mage, buff_case, times)
				dps_0 = tmp[0]/times
				xo=-x_step
				yo=max_ylim
				for i, stat in enumerate(stats_list):
					if i==4:
						xo=0
						yo-=max_ylim
					else:
						xo+=x_step
					mage.stats[stat]-=10
					#print('arcane')
					out = get_dmg(mage, buff_case, times)
					dps_new = out[0]/times
					mage.stats[stat]+=10

					fraction_increase_per_stat = -0.1*(dps_new/dps_0-1)
					#stat_per_percent_fire[stat_per_percent_fire<0]=np.nan
					#stat_per_percent_fire[stat_per_percent_fire>max_ylim]=np.nan
					stat_per_percent = 0.01/fraction_increase_per_stat
					y= 20/stat_per_percent
					y[y<-0.0001] = np.nan
					y[y>max_ylim] = np.nan
					ax.plot(times+xo,y+yo,linestyle= linestyle,color=mage.color)

	xo=-x_step
	yo=max_ylim
	for i, stat in enumerate(stats_list):
		if i==4:
			xo=0
			yo-=max_ylim
		else:
			xo+=x_step
		ax.text(xo+xlim[0]+0.05*x_step, yo+max_ylim-0.05*max_ylim, stats_names[i],ha='left', va='top')
	ax.set_xlim(xlim)
	ax.set_ylim([0,2*max_ylim])
	ax.set_xticks([])
	ax.set_yticks(np.arange(max_ylim*4)/2)
	ax.set_yticklabels(np.arange(max_ylim*4)/2%max_ylim)
	ax.plot(xlim, [max_ylim,max_ylim], lw=0.5,color=[0,0,0,1])
	ax.grid()
	for i in range(1,4):
		ax.plot([xlim[0]+x_step*i]*2, [0,max_ylim*2], lw=0.5,color=[0,0,0,1])
	x_ticks_0 = np.arange((int((times[0]-1)/30)+1)*30,times[-1],30)
	x_ticks = []
	for i in range(4):
		for x in x_ticks_0:
			x_ticks.append(x+i*x_step)
	ax.set_xticks(ticks=x_ticks)
	x_ticks = []
	for i in range(4):
		for x in x_ticks_0:
			x_ticks.append(int(x))
	ax.set_xticklabels(x_ticks)
	ax.set_xlabel('Total casting time before boss dead [s]')
	ax.set_ylabel('Stat weight [-]')




	'''axes[i].set_title(stats_names[i])
	axes[i].set_ylim([0,max_ylim])
	axes[i].set_yticks([0,1,2,3,4,5])
	axes[i].grid()
	axes[i].set_xlim([20,180])'''
	#axes[-1].set_axis_off()
	#fig.suptitle('Stat weights')
	#fig.tight_layout()

def plot_compare_buff_states(ui, mages, buff_cases, linestyles, ax):
		xlim = [ui['time_min'],ui['time_max']]
		times = np.arange(ui['time_min'],ui['time_max']+1, 1)
		max_ylim = ui['stat_weight_ymax']
		ax.plot(times, np.zeros(times.shape), color=[0,0,0,1])
		for mage in mages:
			done_first = 0
			for i, buff_case in enumerate(buff_cases):
				linestyle = linestyles[i]
				if buff_case['check'] == 1:
					if done_first ==0:
						tmp = get_dmg(mage, buff_case, times)
						dps_0 = tmp[0]/times
						done_first = 1
						label_0 = ui['buff_case_'+str(i)+'_label']
					else:
						tmp = get_dmg(mage, buff_case, times)
						dps_1 = tmp[0]/times
						ax.plot(times, 100*(dps_1/dps_0-1), linestyle= linestyle, color=mage.color,
								label = mage.label+', '+ui['buff_case_'+str(i)+'_label'])
		ax.set_xticks(ticks=np.arange((int((times[0]-1)/30)+1)*30,times[-1]+1,30))
		ax.set_xlabel('Total casting time before boss dead [s]')
		ax.set_ylabel('% damage increase vs '+label_0)
		ax.legend()
		ax.set_xlim([ui['time_min'],ui['time_max']])
		ax.grid()

def set_default_mage(event):
	frame = event.widget
	while not hasattr(frame,'nav'):
		frame = frame.master
	frame.nav.clear_color('color3')
	frame.nav.color_selected('color3')
	mages = frame.nav.get_paths_of_selected_items()
	if len(mages)>0:
		frame.default_mage = frame.nav.get_paths_of_selected_items()[0]
		print('set default_mage:',frame.default_mage )
	else:
		delattr(frame,'default_mage')
		print('cleared default_mage' )
	frame.nav.deselect()

def plot_compare_mages(ui, default_mage, mages, buff_cases, linestyles, ax):
		xlim = [ui['time_min'],ui['time_max']]
		times = np.arange(ui['time_min'],ui['time_max']+1, 1)
		max_ylim = ui['stat_weight_ymax']
		ax.plot(times, np.zeros(times.shape), color=default_mage.color)

		for i, buff_case in enumerate(buff_cases):
			linestyle = linestyles[i]
			if buff_case['check'] == 1:
				tmp = get_dmg(default_mage, buff_case, times)
				dps_0 = tmp[0]/times
				for mage in mages:
					if mage.location == default_mage.location:
						continue
					tmp = get_dmg(mage, buff_case, times)
					dps_1 = tmp[0]/times
					ax.plot(times, 100*(dps_1/dps_0-1), linestyle= linestyle, color=mage.color,
							label = mage.label+', '+ui['buff_case_'+str(i)+'_label'])
		ax.set_xticks(ticks=np.arange((int((times[0]-1)/30)+1)*30,times[-1]+1,30))
		ax.grid()
		ax.set_xlabel('Total casting time before boss dead [s]')
		ax.set_ylabel('% damage increase vs '+default_mage.label)
		ax.legend()
		ax.set_xlim([ui['time_min'],ui['time_max']])
