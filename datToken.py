class Token:
    keywords={
        'registration_free':4,
        'friendlyname':5,
        'rowdy_factor':6,
        'model':7,
        'sound':8,
        'varnamelist':9,
        'script':10,
        'constfile':11,
        'add_camera_driver':12,
        'set_camera_std':13,
        'set_camera_outside_center':14,
        'mass':15,
        'momentofintertia':16,
        'boundingbox':17,
        'schwerpunkt':18,
        'rollwiderstand':19,
        'rot_pnt_long':20,
        'inv_min_turnradius':21,
        'ai_deltaheight':22,
        'newachse':23,
        'description':24,
        'end':25,
        'number':26,
        'registration_automatic':27,
        'kmcounter_init':28,
        'sound_ai':29,
        'paths':30,
        'passengercabin':31,
        'stringvarnamelist':32,
        'view_schedule':33,
        'view_ticketselling':34,
        'add_camera_pax':35,
        'add_camera_reflexion':36,
        'add_camera_reflexion_2':37,
        'new_attachment':38,
        'couple_back':39,
        'coupling_back':40,
        'CTC':41,
        'CTCTexture':42,
        'texttexture_enh':43,
        'texttexture':44,
        'mesh':45,
        'viewpoint':46,
        'matl':47,
        'matl_envmap':48,
        'matl_bumpmap':49,
        'matl_transmap':50,
        'alphascale':51,
        'matl_alpha':52,
        'illumination_interior':53,
        'spotlight':54,
        'light_enh_2':55,
        'smoke':56,
        'visible':57,
        'texchanges':58,
        'matl_change':59,
        'texcoordtransY':60,
        'matl_item':61,
        'matl_lightmap':62,
        'matl_texadress_border':63,
        'newanim':64,
        'matl_freetex':65,
        'mouseevent':66,
        'matl_allcolor':67,
        'matl_nightmap':68,
        'useTextTexture':69,
        'matl_texadress_clamp':70,
        'matl_noZwrite':71,
        'matl_noZcheck':72,
        'isshadow':73,
        'const':74,
        'matl_envmap_mask':75,
        'scriptshare':76,
        'LOD':77,
        'interiorlight':78,
        'mesh_ident':79,
        'animparent':80,
        'coupling_front':81,
        'couple_front_open_for_sound':82,
        'coupling_front_character':83,
        'tex_detail_factor':84,
        'scripttexture':85,
        'light_enh':86,
        'smoothskin':87,
        'setbone':88,
        'VFDmaxmin':89,
        'shadow':90,
        'newcurve':91,
        'pnt':92,
        'type':93,
        'fixed':94,
        'control_cable_front':95,
        'control_cable_back':96,
        'boogies':97,
        'sinus':98,
        'rail_body_osc':99,
        'contact_shoe':100,
    }
    revkeywords={v:k for k,v in keywords.items()}
    tags={
        0:'none',
        1:'comment',
        2:'number',
        3:'string'
    }
    tags.update(revkeywords)
    def __init__(self,type:int,value:str) -> None:
        self.type=type
        self.string=value
        if self.type==0:
            try:
                self.value=float(value)
                self.type=2
            except ValueError:
                self.type=3
            return
        if self.type==2:
            try:
                self.type=Token.keywords[self.string]
                self.string=''
            except KeyError:
                self.type=0   

    @property
    def type_name(self):
        return self.tags[self.type]
    def __str__(self) -> str:
        if self.type<4:
            return self.string
        else:
            return self.type_name