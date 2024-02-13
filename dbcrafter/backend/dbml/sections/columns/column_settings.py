class ColumnSetting:
    
    @property
    def name(self) -> str:
        return self.__name
    
    def __init__(self, name: str, value: str="", has_value: bool=True) -> None:
        self.__name = name
        self.value = value
        self.has_value = has_value
        
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, ColumnSetting):
            return False
        return self.__name == __value.name
    
    def __lt__(self, __value: object) -> bool:
        if not isinstance(__value, ColumnSetting):
            return False
        return self.__name < __value.name
    
    def __str__(self) -> str:
        return f"{self.__name}{': '+self.value if self.has_value else ''}"
    
#defining macros for the allowed settings and if they have a value
# the key is the setting name and the value is a tuple with the setting value and if it has a value
# for example: ColumnSettingMacros["primary_key"] -> ("primary_key", False)

ColumnSettingMacros = {
    "note": ColumnSetting(name="note",value="", has_value=True),
    "pk": ColumnSetting(name="pk", value="", has_value=False),
    "unique": ColumnSetting(name="unique", value="", has_value=False),
    "default": ColumnSetting(name="default", value="", has_value=True),
    "not null": ColumnSetting(name="not null", value="", has_value=False),
    "null": ColumnSetting(name="null", value="", has_value=False),
    "increment": ColumnSetting(name="increment", value="", has_value=False),
}

class ColumnSettings:
    
    def __init__(self) -> None:
        self.settings = []
        
    # is a string in the format [setting1, setting2, setting3]
    def __str__(self) -> str:
        return str.format("[{0}]", ', '.join([str(setting) for setting in self.settings])) if len(self.settings) > 0 else ""
    
    def add_setting(self, setting: str) -> None:
        if not (setting in ColumnSettingMacros.keys()):
            raise Exception(f"Setting {setting} is not allowed")
        if setting not in [s.name for s in self.settings]:
            self.settings.append(ColumnSettingMacros[setting])
        else:
            raise Exception(f"Setting {setting} already exists")
            
    
    def __getitem__(self, setting: str) -> ColumnSetting:
        for s in self.settings:
            if s.name == setting:
                return s
        return None
        
    def __delitem__(self, setting: str) -> None:
        for i, s in enumerate(self.settings):
            if s.name == setting:
                del self.settings[i]
                return
            
    # could get the length of the settings like a list len(ColumnSettings)
    def __len__(self) -> int:
        return len(self.settings)
    
    # could iterate over the settings like a list for setting in ColumnSettings
    def __iter__(self) -> ColumnSetting:
        return iter(self.settings)
    
    # could check if a setting is in the settings like a list setting in ColumnSettings
    def __contains__(self, setting: str) -> bool:
        return setting in [s.name for s in self.settings]

        
        
    
    