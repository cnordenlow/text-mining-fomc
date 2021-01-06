

########Plot bubble

###
plot_bubble <- function(temp, x_axis, y_axis,bubble_size, c_title, c_subtitle, c_caption, c_x_axis, c_y_axis){

  
  
  
  
  
#https://gist.github.com/grigory93/f370c5eb997fc74b7b7ec83e73d4dffa#file-ggplot2-data-r

#https://ggrepel.slowkow.com/articles/examples.html
p <- ggplot(data=temp, aes(x = x_axis, y = y_axis)) +
  geom_point(aes(size=bubble_size, color=subject)) +
  #  geom_text(aes(label=subject), size=4,position=position_jitter(width=1,height=2)) +
  geom_text_repel(aes(label=subject),min.segment.length = 0, seed = 42, box.padding = 0.75)+
  #  geom_text(aes(label=subject), size=4, nudge_x=0.0, nudge_y=-0.15,position=position_jitter(width=,height=1)) +
  
  geom_hline(yintercept=0) + geom_vline(xintercept=0) +
  theme_minimal() +
  
  theme(legend.position="bottom",
        plot.caption=element_text(hjust=0),
        plot.subtitle=element_text(face="italic"),
        plot.title=element_text(size=16,face="bold"))+
  
  labs(x=c_x_axis,y=c_y_axis,
       title=c_title,
       subtitle=c_subtitle,
       caption=c_caption)+
  
  theme(legend.position = "none")+
  
  annotate(geom="text", x=max(abs(temp$x_axis))*1.15, y=max(abs(temp$y_axis))*1.25, label="Cooking", color="black",size=4, fontface="italic",hjust = 1)+
  annotate(geom="text", x=max(abs(temp$x_axis))*1.15, y=-max(abs(temp$y_axis))*1.25, label="Fading", color="black",size=4, fontface="italic",hjust = 1)+
  annotate(geom="text", x=-max(abs(temp$x_axis))*1.15, y=-max(abs(temp$y_axis))*1.25, label="In the drawer", color="black",size=4, fontface="italic",hjust = 0)+
  annotate(geom="text", x=-max(abs(temp$x_axis))*1.15, y=max(abs(temp$y_axis))*1.25, label="Up and coming", color="black",size=4, fontface="italic",hjust = 0)




}





plot_line <- function(temp, x_axis, y_axis, hline_intercept, fed_funds_rate, c_title, c_subtitle, c_caption, c_x_axis, c_y_axis){
  
  #####To make the fed funds rate take as much of the plot in all plots. not scale fit
  
  plot_scale = ((max(temp$y_axis))-(min(temp$y_axis)))
  factor = plot_scale / max(temp$fed_funds_rate)
  
  temp <- temp%>%
    mutate(fed_funds_rate = fed_funds_rate * factor / 4)%>%
    mutate(fed_funds_rate = min(temp$y_axis) + fed_funds_rate) #to always begin at the bottom of the plot
  
  
  

p <- ggplot(data=temp, aes(x=x_axis, y=y_axis)) + 
  geom_line(size=1)+
  geom_point(size=2)+
  geom_line( aes(y=fed_funds_rate), size=1, color="blue") +
  
  geom_hline(yintercept=max(temp$hline_intercept), linetype="dashed", color = "red",size=1)+
  theme_light()+
  #  theme_minimal(base_size=8)+
  theme(legend.position="bottom",
        plot.caption=element_text(hjust=0),
        plot.subtitle=element_text(face="italic"),
        plot.title=element_text(size=16,face="bold"))+
  
  labs(x=c_x_axis,y=c_y_axis,
       title=c_title,
       subtitle=c_subtitle,
       caption=c_caption)

}


